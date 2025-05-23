from fastapi import FastAPI, HTTPException, Body, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import json
import aiofiles
from pathlib import Path
from uuid import uuid4

from .models import (
    WorkflowPayload, WorkflowExecutionResponse, AISuggestionRequest, AISuggestionResponse,
    StylePreset, WorkflowTemplate, Node, NodeType, AIProviderKeyConfig
)
from .services import execute_ai_workflow, get_ai_assistant_suggestion, PREDEFINED_STYLES

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
TEMP_UPLOAD_DIR_NAME = os.getenv("TEMP_UPLOAD_DIR", "temp_uploads")
TEMP_UPLOAD_PATH = Path(__file__).parent / TEMP_UPLOAD_DIR_NAME
TEMP_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="MarketCanvas AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Reflex default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(f"/{TEMP_UPLOAD_DIR_NAME}", StaticFiles(directory=TEMP_UPLOAD_PATH), name="temp_uploads")

TEMPLATES_DATA_DIR = Path(__file__).parent / "templates_data"
WORKFLOW_TEMPLATES_CACHE: List[WorkflowTemplate] = []

@app.on_event("startup")
async def startup_event():
    WORKFLOW_TEMPLATES_CACHE.clear() # Clear cache on reload if any
    for file_path in TEMPLATES_DATA_DIR.glob("*.json"):
        try:
            with open(file_path, "r") as f:
                template_data = json.load(f)
                WORKFLOW_TEMPLATES_CACHE.append(WorkflowTemplate(**template_data))
        except Exception as e:
            print(f"Error loading template {file_path.name}: {e}")
    print(f"Loaded {len(WORKFLOW_TEMPLATES_CACHE)} workflow templates.")
    print(f"Available {len(PREDEFINED_STYLES)} style presets.")

@app.get("/")
async def root_info():
    return {"message": "MarketCanvas AI Backend is active."}

@app.post("/api/v1/workflow/execute", response_model=WorkflowExecutionResponse)
async def api_execute_workflow_endpoint(workflow_data: WorkflowPayload = Body(...)):
    if not workflow_data.api_keys:
        return WorkflowExecutionResponse(
            updated_nodes=workflow_data.nodes,
            error="API keys configuration missing in the request payload.",
            execution_log=["Critical Error: API keys configuration not received by backend."]
        )
    try:
        processed_workflow, log = await execute_ai_workflow(workflow_data)
        final_output_url = None
        for node in processed_workflow.nodes: # Find final output from an OutputNode
            if node.type == NodeType.OUTPUT and node.data.get("output_image_url"):
                final_output_url = node.data.get("output_image_url")
                break
        return WorkflowExecutionResponse(
            updated_nodes=processed_workflow.nodes,
            final_output_url=final_output_url,
            execution_log=log,
            error=None # Explicitly None if no error during processing steps
        )
    except Exception as e:
        # This is a fallback for unexpected errors during the endpoint handling itself.
        # Errors within execute_ai_workflow should be part of its returned log/error.
        print(f"Critical unhandled error in /execute endpoint: {e}")
        return WorkflowExecutionResponse(
            updated_nodes=workflow_data.nodes, # Return original nodes on such failure
            error=f"Server error during workflow execution: {str(e)}",
            execution_log=[f"Server Critical Error: {str(e)}"]
        )

@app.post("/api/v1/ai/suggest", response_model=AISuggestionResponse)
async def api_get_ai_suggestion_endpoint(request_data: AISuggestionRequest = Body(...)):
    try:
        suggestion = await get_ai_assistant_suggestion(
            workflow=request_data.current_workflow,
            user_query=request_data.user_query
        )
        return AISuggestionResponse(suggestion_text=suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestion: {str(e)}")

@app.get("/api/v1/styles/presets", response_model=List[StylePreset])
async def get_style_presets_api_endpoint():
    return PREDEFINED_STYLES

@app.get("/api/v1/workflows/templates", response_model=List[WorkflowTemplate])
async def get_workflow_templates_api_endpoint():
    return WORKFLOW_TEMPLATES_CACHE

@app.post("/api/v1/assets/upload")
async def upload_asset_api_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty.")

    # Basic filename sanitization and uniqueness
    sanitized_name = "".join(c for c in Path(file.filename).name if c.isalnum() or c in ['.', '_', '-']).strip()
    if not sanitized_name: sanitized_name = "uploaded_file" # Fallback
    unique_filename = f"{uuid4()}_{sanitized_name}"
    file_path = TEMP_UPLOAD_PATH / unique_filename

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()  # Read content from UploadFile
            await out_file.write(content)
        
        file_url = f"{BACKEND_BASE_URL}/{TEMP_UPLOAD_DIR_NAME}/{unique_filename}"
        return {"file_url": file_url, "file_name": file.filename} # Return original filename for display
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")
