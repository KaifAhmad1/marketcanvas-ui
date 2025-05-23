import reflex as rx
from typing import List, Dict, Any, Optional, cast
import json
import httpx
import random
from pydantic import BaseModel, Field # Can use Pydantic for stricter internal models if preferred

# --- Frontend Data Models (Mirroring backend/models.py where applicable) ---
# Using rx.Base for objects within rx.State lists/dicts for reactivity.

class NodeData(rx.Base):
    label: Optional[str] = ""
    # AI Generation related
    prompt: Optional[str] = ""
    negative_prompt: Optional[str] = ""
    seed: Optional[int] = None
    # Image URLs
    input_image_url: Optional[str] = "" # For ImageInputNode
    base_image_url: Optional[str] = ""  # For ProductInSceneNode
    product_image_url: Optional[str] = "" # For ProductInSceneNode
    style_reference_image_url: Optional[str] = "" # For StyleNode
    output_image_url: Optional[str] = None # Common output
    # Style Node specific
    style_mode: Optional[str] = "preset" # Default for StyleNode
    style_preset_id: Optional[str] = ""
    intensity: Optional[float] = 0.7
    # Image Upload specific
    file_name: Optional[str] = ""
    # Text Overlay specific
    text_content: Optional[str] = "Sample Text"
    font_family: Optional[str] = "Arial"
    font_size: Optional[int] = 48
    font_color: Optional[str] = "#FFFFFF"
    text_x_position_percent: Optional[int] = 50
    text_y_position_percent: Optional[int] = 50
    # Common utility
    error_message: Optional[str] = None
    provider: Optional[str] = "fal_ai" # Default AI provider

class Node(rx.Base):
    id: str
    type: str # Corresponds to NodeType enum value from backend
    position: Dict[str, float]
    data: NodeData = Field(default_factory=NodeData) # Ensure default is NodeData instance
    draggable: bool = True
    connectable: bool = True

class Edge(rx.Base):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None
    animated: bool = True
    label: Optional[str] = "" # e.g., "Image", "Prompt"

class StylePreset(rx.Base):
    id: str
    name: str
    description: Optional[str] = ""
    thumbnail_url: Optional[str] = ""
    parameters: Dict[str, Any] = {}

class WorkflowTemplate(rx.Base):
    id: str
    name: str
    description: Optional[str] = ""
    category: Optional[str] = ""
    thumbnail_url: Optional[str] = ""
    workflow_payload: Dict[str, Any] = {} # Stores nodes and edges as dicts

class AIProviderKeys(rx.Base):
    fal_ai_key: str = ""
    google_gemini_key: str = ""
    stability_ai_key: str = ""
    pipecat_api_key: str = "" # For AI assistant if it uses a separate key
    # blackforest_flux_key: str = "" # Example for future

class AppState(rx.State):
    # Core Canvas State
    nodes: List[Node] = []
    edges: List[Edge] = []
    selected_node_id: Optional[str] = None

    # UI & Interaction State
    live_preview_image_url: Optional[str] = None
    is_loading_workflow: bool = False
    workflow_execution_log: List[str] = []
    workflow_error_message: Optional[str] = None
    ai_assistant_suggestion: Optional[str] = ""
    is_loading_suggestion: bool = False
    current_ui_theme: str = "light" # "light" or "dark"
    show_api_key_modal: bool = False
    _react_flow_instance: Optional[Any] = None # Store JS ReactFlow instance if needed

    # Data fetched from backend
    available_style_presets: List[StylePreset] = []
    available_workflow_templates: List[WorkflowTemplate] = []

    # Asset Management
    uploaded_asset_url: Optional[str] = None # URL of the last successfully uploaded asset
    is_uploading_asset: bool = False

    # User-provided API Keys (stored in browser session memory)
    api_keys: AIProviderKeys = Field(default_factory=AIProviderKeys)

    backend_url: str = "http://localhost:8000"

    # --- Lifecycle & Initial Data ---
    async def on_app_load(self):
        await self.fetch_style_presets()
        await self.fetch_workflow_templates()
        # Load API keys from sessionStorage if they exist
        # This requires JS interop or careful handling if Reflex has a direct way.
        # For simplicity, we'll rely on user re-entering if session is lost.
        # A more persistent way is localStorage, but with security caveats.
        if not self.nodes: # Default welcome canvas
            self.add_node("imageUpload", "Upload Product", {"x": 100, "y": 150})
            self.add_node("textToImage", "AI Background", {"x": 100, "y": 350}, initial_data={"prompt": "modern studio backdrop"})
            self.add_node("outputNode", "Final Image", {"x": 400, "y": 250})

    async def fetch_style_presets(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/v1/styles/presets")
                response.raise_for_status()
                self.available_style_presets = [StylePreset(**p) for p in response.json()]
        except Exception as e:
            self.workflow_error_message = f"Failed to fetch styles: {str(e)}"

    async def fetch_workflow_templates(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/v1/workflows/templates")
                response.raise_for_status()
                self.available_workflow_templates = [WorkflowTemplate(**t) for t in response.json()]
        except Exception as e:
            self.workflow_error_message = f"Failed to fetch templates: {str(e)}"

    # --- Computed Vars ---
    @rx.var
    def selected_node(self) -> Optional[Node]:
        return next((n for n in self.nodes if n.id == self.selected_node_id), None) if self.selected_node_id else None

    @rx.var
    def nodes_for_reactflow(self) -> List[Dict[str, Any]]:
        return [n.dict(exclude_none=True) for n in self.nodes]

    @rx.var
    def edges_for_reactflow(self) -> List[Dict[str, Any]]:
        return [e.dict(exclude_none=True) for e in self.edges]

    # --- ReactFlow Event Handlers ---
    def on_react_flow_init(self, instance: Any): self._react_flow_instance = instance

    def on_nodes_change(self, changes: List[Dict[str, Any]]):
        # This implements a simplified version of ReactFlow's applyNodeChanges
        new_nodes = self.nodes.copy() # Operate on a mutable copy
        nodes_to_remove_ids = set()

        for change in changes:
            node_id = change.get("id")
            if not node_id: continue

            idx = next((i for i, n in enumerate(new_nodes) if n.id == node_id), -1)

            if change["type"] == "select":
                self.selected_node_id = node_id if change["selected"] else (None if self.selected_node_id == node_id else self.selected_node_id)
            elif change["type"] == "position" and idx != -1 and change.get("position"):
                # Recreate node object for full reactivity on nested position dict
                old_node = new_nodes[idx]
                new_nodes[idx] = Node(**{**old_node.dict(), "position": change["position"]})
            elif change["type"] == "remove":
                nodes_to_remove_ids.add(node_id)
                if self.selected_node_id == node_id: self.selected_node_id = None
        
        if nodes_to_remove_ids:
            self.nodes = [n for n in new_nodes if n.id not in nodes_to_remove_ids]
            self.edges = [e for e in self.edges if e.source not in nodes_to_remove_ids and e.target not in nodes_to_remove_ids]
        else:
            self.nodes = new_nodes # Assign back if only positions/selections changed

        # Ensure selected_node_id is valid
        if self.selected_node_id and not any(n.id == self.selected_node_id for n in self.nodes):
            self.selected_node_id = None

    def on_edges_change(self, changes: List[Dict[str, Any]]):
        new_edges = self.edges.copy()
        edges_to_remove_ids = set()
        for change in changes:
            edge_id = change.get("id")
            if not edge_id: continue
            if change["type"] == "remove": edges_to_remove_ids.add(edge_id)
        if edges_to_remove_ids: self.edges = [e for e in new_edges if e.id not in edges_to_remove_ids]
        else: self.edges = new_edges


    def on_connect(self, connection: Dict[str, Any]):
        s, t = connection.get("source"), connection.get("target")
        sh, th = connection.get("sourceHandle"), connection.get("targetHandle")
        if s and t:
            new_id = f"e_{s}{'_'+sh if sh else ''}-{t}{'_'+th if th else ''}_{random.randint(0,9999)}"
            if not any(e.id == new_id or (e.source==s and e.target==t and e.sourceHandle==sh and e.targetHandle==th) for e in self.edges):
                self.edges.append(Edge(id=new_id, source=s, target=t, sourceHandle=sh, targetHandle=th))

    def on_node_click_rf(self, node_data: Dict[str, Any]): self.selected_node_id = node_data.get("id")
    def on_pane_click_rf(self): self.selected_node_id = None
    def on_node_drag_stop_rf(self, node_data: Dict[str, Any]): pass # Position updated via on_nodes_change

    # --- Node & Workflow Management ---
    def _generate_unique_id(self, prefix: str) -> str: return f"{prefix}_{random.randint(10000, 99999)}"

    def add_node(self, node_type: str, label_prefix: str, position: Optional[Dict[str, float]] = None, initial_data: Optional[Dict[str, Any]] = None):
        node_id = self._generate_unique_id("node")
        pos = position or {"x": random.randint(100, 500), "y": random.randint(100, 300)}
        
        node_data_obj = NodeData(**(initial_data or {}))
        if not node_data_obj.label: # Set default label
            node_data_obj.label = f"{label_prefix} #{len(self.nodes) + 1}"
        # Set default provider if node type supports it and not already set
        if node_type == "textToImage" and not node_data_obj.provider:
            node_data_obj.provider = "fal_ai"

        new_node = Node(id=node_id, type=node_type, position=pos, data=node_data_obj)
        self.nodes.append(new_node)
        self.selected_node_id = node_id

    def delete_selected_node(self):
        if self.selected_node_id:
            node_id_to_delete = self.selected_node_id
            self.nodes = [n for n in self.nodes if n.id != node_id_to_delete]
            self.edges = [e for e in self.edges if e.source != node_id_to_delete and e.target != node_id_to_delete]
            self.selected_node_id = None

    def update_selected_node_data(self, field_name: str, value: Any):
        if not self.selected_node_id: return
        idx = next((i for i, n in enumerate(self.nodes) if n.id == self.selected_node_id), -1)
        if idx != -1:
            current_node = self.nodes[idx]
            new_data_dict = current_node.data.dict()
            new_data_dict[field_name] = value
            
            updated_node_data_obj = NodeData(**new_data_dict)
            # Create a new Node instance for Reflex to detect the change
            self.nodes[idx] = Node(
                id=current_node.id, type=current_node.type, position=current_node.position,
                data=updated_node_data_obj, draggable=current_node.draggable, connectable=current_node.connectable
            )

    def load_workflow_from_template(self, template_id: str):
        template = next((t for t in self.available_workflow_templates if t.id == template_id), None)
        if template and template.workflow_payload:
            self.nodes = [Node(**n_dict) for n_dict in template.workflow_payload.get("nodes", [])]
            self.edges = [Edge(**e_dict) for e_dict in template.workflow_payload.get("edges", [])]
            self.selected_node_id = None; self.live_preview_image_url = None
            self.workflow_execution_log = [f"Loaded template: {template.name}"]
            self.workflow_error_message = None

    # --- UI Theme ---
    def set_ui_theme(self, theme_name: str): self.current_ui_theme = theme_name

    # --- API Key Management ---
    def toggle_api_key_modal(self): self.show_api_key_modal = not self.show_api_key_modal
    
    def set_api_key(self, provider_name_key: str, key_value: str):
        current_keys_dict = self.api_keys.dict()
        current_keys_dict[provider_name_key] = key_value
        self.api_keys = AIProviderKeys(**current_keys_dict)
        # Optionally try to persist to sessionStorage via rx.call_script for this browser session
        # yield rx.call_script(f"sessionStorage.setItem('mcanvas_apikeys', JSON.stringify({self.api_keys.json()}))")


    # --- Asset Upload ---
    async def handle_asset_upload(self, files: List[rx.UploadFile]):
        if not files: return
        self.is_uploading_asset = True; self.uploaded_asset_url = None; self.workflow_error_message = None
        try:
            file_to_upload = files[0]
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/v1/assets/upload",
                    files={"file": (file_to_upload.filename, await file_to_upload.read(), file_to_upload.content_type)},
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                self.uploaded_asset_url = result.get("file_url")

                if self.selected_node and self.selected_node.type == "imageUpload" and self.uploaded_asset_url:
                    self.update_selected_node_data("output_image_url", self.uploaded_asset_url)
                    self.update_selected_node_data("file_name", result.get("file_name", file_to_upload.filename))
                elif self.uploaded_asset_url: # Add a new ImageUpload node if none is selected or wrong type
                    self.add_node(
                        node_type="imageUpload",
                        label_prefix=result.get("file_name", file_to_upload.filename).split('.')[0],
                        initial_data={"output_image_url": self.uploaded_asset_url, "file_name": result.get("file_name", file_to_upload.filename)}
                    )
        except Exception as e:
            self.workflow_error_message = f"Upload failed: {str(e)}"
        finally:
            self.is_uploading_asset = False

    # --- Backend Interaction ---
    async def execute_workflow(self):
        self.is_loading_workflow = True; self.workflow_error_message = None
        self.workflow_execution_log = ["Sending workflow to backend..."]; self.live_preview_image_url = None

        payload = {
            "nodes": [n.dict(exclude_none=True) for n in self.nodes],
            "edges": [e.dict(exclude_none=True) for e in self.edges],
            "api_keys": self.api_keys.dict(exclude_none=True) # Send API keys
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.backend_url}/api/v1/workflow/execute", json=payload, timeout=300.0) # Long timeout
                response.raise_for_status()
                result_data = response.json()

                self.workflow_execution_log.extend(result_data.get("execution_log", []))

                if result_data.get("error"):
                    self.workflow_error_message = result_data["error"]
                else:
                    # Update nodes based on backend response. Important to recreate for reactivity.
                    backend_nodes_map = {bn_dict["id"]: bn_dict for bn_dict in result_data.get("updated_nodes", [])}
                    updated_nodes_list = []
                    for fe_node in self.nodes:
                        if fe_node.id in backend_nodes_map:
                            updated_nodes_list.append(Node(**backend_nodes_map[fe_node.id]))
                        else: # Should ideally not happen if backend returns all nodes
                            updated_nodes_list.append(fe_node)
                    self.nodes = updated_nodes_list
                    
                    self.live_preview_image_url = result_data.get("final_output_url")
                    if not self.live_preview_image_url: # Fallback to first available output
                        for node_dict_res in result_data.get("updated_nodes", []):
                            if node_dict_res.get("data", {}).get("output_image_url"):
                                self.live_preview_image_url = node_dict_res["data"]["output_image_url"]
                                break
                    self.workflow_execution_log.append("Workflow execution successful.")

        except httpx.HTTPStatusError as e:
            self.workflow_error_message = f"API Error ({e.response.status_code}): {e.response.text}"
        except httpx.RequestError as e:
            self.workflow_error_message = f"Network Error: Could not connect to backend ({e.request.url})."
        except Exception as e:
            self.workflow_error_message = f"An unexpected error occurred during execution: {str(e)}"
        finally:
            self.is_loading_workflow = False
            if self.workflow_error_message and self.workflow_error_message not in self.workflow_execution_log:
                self.workflow_execution_log.append(f"Error: {self.workflow_error_message}")

    async def fetch_ai_suggestion(self, user_query: Optional[str] = None):
        self.is_loading_suggestion = True; self.ai_assistant_suggestion = ""
        payload = {
            "user_query": user_query,
            "current_workflow": {
                 "nodes": [n.dict(exclude_none=True) for n in self.nodes],
                 "edges": [e.dict(exclude_none=True) for e in self.edges],
                 "api_keys": self.api_keys.dict(exclude_none=True) # Pass keys if assistant needs them
            } if self.nodes else None
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.backend_url}/api/v1/ai/suggest", json=payload, timeout=60.0)
                response.raise_for_status()
                result = response.json()
                self.ai_assistant_suggestion = result.get("suggestion_text", "No suggestion available at the moment.")
        except Exception as e:
            self.ai_assistant_suggestion = f"Error fetching AI suggestion: {str(e)}"
        finally:
            self.is_loading_suggestion = False
