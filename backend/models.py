from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from uuid import uuid4

class NodeType(str, Enum):
    IMAGE_UPLOAD = "imageUpload"
    IMAGE_INPUT = "imageInput"
    TEXT_TO_IMAGE = "textToImage"
    PRODUCT_IN_SCENE = "productInScene"
    STYLE_APPLY = "styleApply"
    CROP_RESIZE = "cropResize"
    TEXT_OVERLAY = "textOverlay"
    OUTPUT = "outputNode"

class StyleApplicationMode(str, Enum):
    PRESET = "preset"
    IMAGE_REFERENCE = "image_reference"

class BaseNodeData(BaseModel):
    label: Optional[str] = None
    output_image_url: Optional[str] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None # For nodes supporting multiple AI backends

class ImageUploadNodeData(BaseNodeData):
    file_name: Optional[str] = None

class ImageInputNodeData(BaseNodeData):
    input_image_url: Optional[str] = None

class TextToImageNodeData(BaseNodeData):
    prompt: str = "A stunning futuristic cityscape at dusk"
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None
    # provider field inherited from BaseNodeData, e.g., "fal_ai", "google_gemini", "stability_ai"

class ProductInSceneNodeData(BaseNodeData):
    base_image_url: Optional[str] = None
    product_image_url: Optional[str] = None
    prompt: str = "Integrate the product naturally into the scene, matching lighting and perspective."

class StyleNodeData(BaseNodeData):
    style_mode: StyleApplicationMode = StyleApplicationMode.PRESET
    style_preset_id: Optional[str] = None
    style_reference_image_url: Optional[str] = None
    intensity: float = Field(default=0.7, ge=0.0, le=1.0)

class CropResizeNodeData(BaseNodeData):
    crop_x: Optional[int] = 0
    crop_y: Optional[int] = 0
    crop_width: Optional[int] = None
    crop_height: Optional[int] = None
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
    keep_aspect_ratio: bool = True

class TextOverlayNodeData(BaseNodeData):
    text_content: str = "Your Awesome Text Here!"
    font_family: str = "Arial, sans-serif"
    font_size: int = 48
    font_color: str = "#FFFFFF"
    text_x_position_percent: int = Field(default=50, ge=0, le=100) # Position as percentage
    text_y_position_percent: int = Field(default=50, ge=0, le=100)
    background_color: Optional[str] = None # e.g., "#00000080" for semi-transparent black
    text_alignment: str = "center" # "left", "center", "right"

class OutputNodeData(BaseNodeData):
    pass

class Node(BaseModel):
    id: str
    type: NodeType
    position: Dict[str, float]
    data: Dict[str, Any] = Field(default_factory=dict) # Parsed into specific NodeData in services
    width: Optional[int] = 180
    height: Optional[int] = None # Auto based on content or fixed if needed
    selected: Optional[bool] = None
    dragging: Optional[bool] = None
    draggable: Optional[bool] = True
    connectable: Optional[bool] = True

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None # e.g., "outputImage", "value"
    targetHandle: Optional[str] = None # e.g., "inputImage", "baseImage"
    animated: bool = True
    label: Optional[str] = None

class AIProviderKeyConfig(BaseModel):
    fal_ai_key: Optional[str] = None
    google_gemini_key: Optional[str] = None
    stability_ai_key: Optional[str] = None
    pipecat_api_key: Optional[str] = None # For AI assistant
    # blackforest_flux_key: Optional[str] = None # Example for future extension

class WorkflowPayload(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    api_keys: AIProviderKeyConfig # User-provided API keys are now mandatory for execution

class WorkflowExecutionResponse(BaseModel):
    updated_nodes: List[Node]
    final_output_url: Optional[str] = None
    execution_log: List[str] = Field(default_factory=list)
    error: Optional[str] = None

class AISuggestionRequest(BaseModel):
    current_workflow: Optional[WorkflowPayload] = None # api_keys within current_workflow can be used
    user_query: Optional[str] = None

class AISuggestionResponse(BaseModel):
    suggestion_text: Optional[str] = None

class StylePreset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict) # e.g., {"prompt_suffix": "...", "model_id": "..."}

class WorkflowTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    workflow_payload: WorkflowPayload # Note: this internal payload won't have user api_keys
