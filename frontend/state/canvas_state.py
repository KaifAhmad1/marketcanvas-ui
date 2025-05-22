# frontend/state/canvas_state.py
import reflex as rx
from typing import Any, Dict, List, Optional
import random
import json # Not used, can be removed if no direct JSON ops
import datetime

# Enhanced initial nodes with more variety
initial_nodes = [
    {
        "id": "1",
        "type": "input",
        "data": {"label": "Base Image", "image_url": "", "filters": [], "brightness": 100, "contrast": 100},
        "position": {"x": 100, "y": 50},
        "style": {"background": "#1e40af", "color": "white", "border": "2px solid #3b82f6", "borderRadius": "12px"}
    },
    {
        "id": "2",
        "type": "default",
        "data": {"label": "Style Node", "style": "Modern", "intensity": 0.7, "color_palette": ["#3b82f6", "#8b5cf6"]},
        "position": {"x": 300, "y": 125},
        "style": {"background": "#7c3aed", "color": "white", "border": "2px solid #a855f7", "borderRadius": "12px"}
    },
    {
        "id": "3",
        "type": "output",
        "data": {"label": "AI Generator", "model": "DALL-E 3", "prompt": "", "steps": 50},
        "position": {"x": 500, "y": 100},
        "style": {"background": "#059669", "color": "white", "border": "2px solid #10b981", "borderRadius": "12px"}
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2", "animated": True, "style": {"stroke": "#3b82f6", "strokeWidth": 2}},
    {"id": "e2-3", "source": "2", "target": "3", "animated": True, "style": {"stroke": "#8b5cf6", "strokeWidth": 2}},
]

class CanvasState(rx.State):
    # Canvas Data
    nodes: List[Dict[str, Any]] = initial_nodes
    edges: List[Dict[str, Any]] = initial_edges
    selected_node: Dict[str, Any] = {} # Ensure this is properly typed if it holds complex objects
    selected_nodes: List[str] = [] # Should store node IDs as strings

    # Preview & Generation
    preview_image: str = ""
    generated_images: List[Dict[str, Any]] = []
    generation_history: List[Dict[str, Any]] = []

    # Styles & Themes
    current_style: str = "Modern"
    current_tone: str = "Professional"
    available_styles: List[str] = ["Modern", "Vintage", "Minimalist", "Luxury", "Cyberpunk", "Artistic", "Corporate", "Playful"]
    available_tones: List[str] = ["Professional", "Casual", "Elegant", "Bold", "Friendly", "Mysterious", "Energetic", "Calm"]
    theme: str = "dark" # This should ideally control rx.App's theme
    accent_color: str = "#3b82f6" # For Radix theme
    theme_background: str = "#1f2937" # Used for ReactFlow background
    custom_themes: Dict[str, Dict[str, str]] = {}

    # UI States (Ensure these are Vars if they control UI and change dynamically)
    # For simplicity, making them plain Python types first. If they need to be reactive from UI components,
    # they would need to be rx.Var, or methods would update them and trigger re-renders.
    show_context_menu: bool = False # This was in enhanced_canvas.py properties_panel, assumed boolean
    show_tutorial: bool = False
    show_settings: bool = False
    show_export_modal: bool = False
    show_save_dialog: bool = False
    show_load_dialog: bool = False
    show_collaboration_panel: bool = False
    show_properties_panel: bool = True # Added for enhanced_canvas.py
    show_layers_panel: bool = True     # Added for enhanced_canvas.py
    show_ab_test_modal: bool = False   # Added for editor.py

    # Tutorial System
    tutorial_step: int = 0
    tutorial_active: bool = False
    tutorial_type: str = "basic"

    # Analytics & Usage
    analytics: Dict[str, int] = {
        "nodes_created": 0,
        "images_generated": 0,
        "ab_tests_run": 0,
        "exports_made": 0,
        "time_spent": 0 # This would need a timer mechanism
    }

    # A/B Testing
    ab_test_results: List[Dict[str, Any]] = []
    current_ab_test: Dict[str, Any] = {} # Stores info about the currently configured/running A/B test

    # Templates & Projects
    saved_projects: List[Dict[str, Any]] = []
    templates: List[Dict[str, Any]] = [
        {"id": "social_media", "name": "Social Media Post", "category": "Social", "preview": "/placeholder/400/400.svg?text=Social"}, # Using placeholder.svg
        {"id": "banner_ad", "name": "Banner Ad", "category": "Advertising", "preview": "/placeholder/728/90.svg?text=Banner"},
        {"id": "logo_design", "name": "Logo Design", "category": "Branding", "preview": "/placeholder/300/300.svg?text=Logo"},
    ]
    selected_template: str = ""
    active_settings_tab: str = "general" # For settings page tabs

    # AI Models & Settings
    available_models: List[Dict[str, Any]] = [
        {"id": "dalle3", "name": "DALL-E 3", "provider": "OpenAI", "speed": "Medium", "quality": "High"},
        {"id": "midjourney", "name": "Midjourney", "provider": "Midjourney", "speed": "Slow", "quality": "Excellent"},
        {"id": "stable_diffusion", "name": "Stable Diffusion XL", "provider": "Stability AI", "speed": "Fast", "quality": "Good"},
    ]
    selected_model: str = "dalle3"
    model_settings: Dict[str, Any] = {
        "guidance_scale": 7.5,
        "steps": 50,
        "seed": -1, # -1 often means random seed
        "batch_size": 1
    }

    # Collaboration
    collaborators: List[Dict[str, Any]] = []
    current_user: Dict[str, str] = {"id": "user_default_1", "name": "Default User", "role": "owner", "avatar": "/placeholder/40/40.svg?text=U"}
    project_permissions: Dict[str, bool] = {"can_edit": True, "can_export": True, "can_share": True} # Permissions for current_user on current project

    # Text & Overlays (If these are separate elements on a canvas, not nodes)
    text_overlays: List[Dict[str, Any]] = []
    selected_overlay: Optional[int] = None # Index of selected overlay

    # Filters & Effects (Available options for nodes or direct application)
    available_filters: List[str] = ["None", "Blur", "Sharpen", "Vintage", "B&W", "Sepia", "Vignette"]
    available_effects: List[str] = ["None", "Drop Shadow", "Glow", "Emboss", "3D", "Neon"]

    # Export Settings
    export_formats: List[str] = ["PNG", "JPG", "SVG", "PDF"]
    export_sizes: List[str] = ["Original", "1080x1080 (Square)", "1200x630 (Landscape)", "Custom"]
    selected_export_format: str = "PNG"
    selected_export_size: str = "Original"
    custom_width: int = 1024
    custom_height: int = 1024

    # Advanced Features
    version_history: List[Dict[str, Any]] = []
    current_version: int = 0 # Start at 0, first save becomes 1
    auto_save_enabled: bool = True
    grid_enabled: bool = True
    snap_to_grid: bool = True # This needs ReactFlow prop integration
    rulers_enabled: bool = False
    zoom_level: float = 1.0 # Can be controlled by ReactFlow or set here

    # Performance & Quality
    render_quality: str = "High"
    real_time_preview: bool = True # For things like filter adjustments
    gpu_acceleration: bool = True # Hypothetical setting

    # <<< --- ADD THIS COMPUTED VAR --- >>>
    @rx.var
    def has_saved_projects(self) -> bool:
        return len(self.saved_projects) > 0
    # <<< --- END OF ADDITION --- >>>

    # Node Management Methods
    def _create_node_id(self) -> str:
        # Find the highest existing integer ID and increment
        max_id = 0
        for node in self.nodes:
            try:
                node_id_int = int(node["id"])
                if node_id_int > max_id:
                    max_id = node_id_int
            except ValueError:
                # Handle non-integer IDs if they can exist, or ensure IDs are always numeric strings
                pass # For now, assume IDs can be converted to int for this logic
        return str(max_id + 1)

    def _get_default_node_style(self, node_type: str) -> Dict[str, str]:
        base_style = {"color": "white", "borderRadius": "12px"}
        # More specific styles based on node type
        type_styles = {
            "input": {"background": "#1D4ED8", "border": "2px solid #3B82F6"},  # Blue
            "output": {"background": "#059669", "border": "2px solid #10B981"}, # Green
            "default": {"background": "#7C3AED", "border": "2px solid #A78BFA"},# Purple (for style, filter etc.)
            "text": {"background": "#D97706", "border": "2px solid #F59E0B"},    # Amber (for text)
            "ai_processor": {"background": "#DC2626", "border": "2px solid #EF4444"}, # Red (for AI gen)
            "ab_test": {"background": "#EA580C", "border": "2px solid #F97316"}, # Orange (for A/B test)
        }
        return {**base_style, **type_styles.get(node_type, type_styles["default"])}


    def add_node_by_type(self, node_type_str: str, data: Optional[Dict[str, Any]] = None):
        new_node_id = self._create_node_id()
        base_data = {"label": f"{node_type_str.replace('_', ' ').title()} Node"}
        if data:
            base_data.update(data)

        node_config = {
            "input": {"type": "input", "data": {"label": "Base Image", "image_url": "", "brightness": 100, "contrast": 100, "saturation": 100}},
            "style": {"type": "default", "data": {"label": "Style Node", "style_name": "Modern", "intensity": 0.7}},
            "ai_processor": {"type": "default", "data": {"label": "AI Generator", "model_id": self.selected_model, "prompt": ""}},
            "text": {"type": "default", "data": {"label": "Text Overlay", "text_content": "Your Text Here", "font_size": 24}},
            "filter": {"type": "default", "data": {"label": "Image Filter", "filter_type": "None", "strength": 0.5}},
            "ab_test": {"type": "default", "data": {"label": "A/B Test", "variants_count": 2}},
            "output": {"type": "output", "data": {"label": "Final Output"}},
        }

        config = node_config.get(node_type_str, {"type": "default", "data": {"label": "Custom Node"}})
        final_data = config["data"].copy()
        if data: # Allow overriding defaults with provided data
            final_data.update(data)

        new_node = {
            "id": new_node_id,
            "type": config["type"],
            "data": final_data,
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": self._get_default_node_style(node_type_str) # Use specific style
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_base_image_node(self): self.add_node_by_type("input")
    def add_style_node(self): self.add_node_by_type("style")
    def add_ai_processor_node(self): self.add_node_by_type("ai_processor")
    def add_text_node(self): self.add_node_by_type("text")
    def add_filter_node(self): self.add_node_by_type("filter")
    def add_ab_test_node(self): self.add_node_by_type("ab_test")
    def add_output_node(self): self.add_node_by_type("output")


    # Canvas Operations
    def clear_canvas(self):
        self.nodes = []
        self.edges = []
        self.selected_node = {}
        self.selected_nodes = []
        self.preview_image = ""
        self.text_overlays = [] # Assuming this is for non-node overlays
        self._save_version()
        print("Canvas cleared.")

    def duplicate_selected_nodes(self):
        if not self.selected_nodes:
            print("No nodes selected to duplicate.")
            return
        newly_added_nodes = []
        for node_id_str in self.selected_nodes: # Iterate over a copy if modifying
            original_node = next((n for n in self.nodes if n["id"] == node_id_str), None)
            if original_node:
                new_node_id = self._create_node_id() # Use consistent ID generation
                # Deep copy data to avoid shared references if it's complex
                new_data = json.loads(json.dumps(original_node["data"]))
                new_node = {
                    "id": new_node_id,
                    "type": original_node["type"],
                    "data": new_data,
                    "position": {
                        "x": original_node["position"]["x"] + 40, # Smaller offset
                        "y": original_node["position"]["y"] + 40
                    },
                    "style": original_node.get("style", {}).copy()
                }
                newly_added_nodes.append(new_node)
        if newly_added_nodes:
            self.nodes.extend(newly_added_nodes)
            self.analytics["nodes_created"] += len(newly_added_nodes)
            self._save_version()
            self.selected_nodes = [n["id"] for n in newly_added_nodes] # Select the new nodes
            if len(self.selected_nodes) == 1:
                self.select_node(self.selected_nodes[0])
            print(f"Duplicated {len(newly_added_nodes)} node(s).")


    def delete_selected_nodes(self):
        if not self.selected_nodes:
            print("No nodes selected to delete.")
            return
        
        ids_to_delete_str = set(self.selected_nodes) # Use a set for efficient lookup
        
        original_node_count = len(self.nodes)
        self.nodes = [n for n in self.nodes if n["id"] not in ids_to_delete_str]
        deleted_count = original_node_count - len(self.nodes)

        # Remove edges connected to deleted nodes
        self.edges = [e for e in self.edges if e["source"] not in ids_to_delete_str and e["target"] not in ids_to_delete_str]
        
        self.selected_nodes = []
        self.selected_node = {}
        if deleted_count > 0:
            self._save_version()
            print(f"Deleted {deleted_count} node(s).")


    def group_selected_nodes(self):
        if len(self.selected_nodes) <= 1:
            print("Select more than one node to group.")
            return

        group_id = f"group_{self._create_node_id()}" # More unique group ID
        # Ensure selected_nodes are strings
        children_ids = [str(nid) for nid in self.selected_nodes]
        group_bounds = self._calculate_group_bounds(children_ids)

        group_node = {
            "id": group_id,
            "type": "group", # ReactFlow needs this type to be registered or handled
            "data": {
                "label": f"Group ({len(children_ids)} nodes)",
            },
            "position": group_bounds["position"],
            "style": { # Style for the group node itself
                "backgroundColor": "rgba(107, 114, 128, 0.1)", # Tailwind gray-500 with opacity
                "borderColor": "rgb(156, 163, 175)", # Tailwind gray-400
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "8px",
                "width": group_bounds["width"], # Pass as number, ReactFlow converts
                "height": group_bounds["height"],
                # "zIndex": -1 # Ensure it's behind other nodes
            },
            # "childNodes": children_ids, # If your ReactFlow setup uses this for parenting
        }
        # For ReactFlow, you might not add children directly to group node data.
        # Instead, child nodes have a 'parentNode' attribute and 'extent: "parent"'
        
        # Update children to belong to the group
        updated_nodes = []
        group_x, group_y = group_node["position"]["x"], group_node["position"]["y"]
        for node in self.nodes:
            if node["id"] in children_ids:
                node["parentNode"] = group_id
                node["extent"] = "parent"
                # Adjust child position to be relative to the group node's top-left
                # This requires careful handling if ReactFlow doesn't do it automatically
                # node["position"] = {
                #     "x": node["position"]["x"] - group_x,
                #     "y": node["position"]["y"] - group_y,
                # }
            updated_nodes.append(node)
        
        self.nodes = updated_nodes
        self.nodes.append(group_node) # Add group node after updating children

        self.selected_nodes = [group_id] # Select the group
        self.select_node(group_id)
        self._save_version()
        print(f"Grouped {len(children_ids)} nodes into group {group_id}.")

    def _calculate_group_bounds(self, node_ids: List[str]) -> Dict[str, Any]:
        selected_node_objects = [n for n in self.nodes if n["id"] in node_ids]
        if not selected_node_objects:
            return {"position": {"x": 0, "y": 0}, "width": 200, "height": 100} # Default

        # Get actual node dimensions if possible (ReactFlow might provide these)
        # For now, approximate or use fixed values if not available
        get_node_width = lambda node: node.get("width", 150) # Approx. from ReactFlow if rendered
        get_node_height = lambda node: node.get("height", 50) # Approx.

        min_x = min(n["position"]["x"] for n in selected_node_objects)
        min_y = min(n["position"]["y"] for n in selected_node_objects)
        max_x = max(n["position"]["x"] + get_node_width(n) for n in selected_node_objects)
        max_y = max(n["position"]["y"] + get_node_height(n) for n in selected_node_objects)

        padding = 30 # Padding around the content for the group box
        return {
            "position": {"x": min_x - padding, "y": min_y - padding},
            "width": (max_x - min_x) + (2 * padding),
            "height": (max_y - min_y) + (2 * padding)
        }

    # Connection Management
    def on_connect(self, connection: Dict[str, str]):
        source_id = connection.get("source")
        target_id = connection.get("target")
        source_handle = connection.get("sourceHandle") # Optional
        target_handle = connection.get("targetHandle") # Optional

        if not source_id or not target_id:
            print("Invalid connection data received.")
            return

        # Prevent self-loops by default unless specifically allowed
        if source_id == target_id:
            print("Self-loops are not allowed.")
            return

        new_edge_id = f"e_{source_id}{source_handle or ''}-{target_id}{target_handle or ''}"
        
        # Check for existing edge between same nodes (or same handles if specific)
        if any(e["id"] == new_edge_id for e in self.edges):
            print(f"Edge {new_edge_id} already exists.")
            return

        new_edge = {
            "id": new_edge_id,
            "source": source_id,
            "target": target_id,
            "sourceHandle": source_handle,
            "targetHandle": target_handle,
            "animated": True,
            "style": {"stroke": self.accent_color, "strokeWidth": 2},
            "label": self._get_edge_label(source_id, target_id)
        }
        self.edges.append(new_edge)
        self._save_version()
        print(f"Edge created: {new_edge_id}")


    def _get_edge_label(self, source_id: str, target_id: str) -> str:
        source_node = next((n for n in self.nodes if n["id"] == source_id), None)
        # target_node = next((n for n in self.nodes if n["id"] == target_id), None) # Not used currently

        if source_node:
            label_lower = source_node.get("data", {}).get("label", "").lower()
            if source_node.get("type") == "input": return "Data Flow"
            if "style" in label_lower: return "Apply Style"
            if "filter" in label_lower: return "Apply Filter"
        return "" # Default to no label or a generic "Connects"


    def on_nodes_change(self, changes: List[Dict[str, Any]]):
        # This is a simplified handler. ReactFlow provides detailed changes.
        # For a Reflex app, often you just need to ensure the `self.nodes` Var reflects these.
        # The ReactFlow component should be bound to `CanvasState.nodes`.
        # However, selection changes might need explicit handling here.

        new_selected_nodes_ids = []
        node_to_select_singularly = None

        for change in changes:
            if change["type"] == "select":
                node_id = change["id"]
                if change["selected"]:
                    new_selected_nodes_ids.append(node_id)
                # If a node is deselected, it's removed from ReactFlow's selection.
                # We sync our selected_nodes list.
            elif change["type"] == "position":
                # If only position changed, and nodes Var is bound, Reflex handles it.
                # But if you need to react to position change (e.g. save version), do it here.
                # For group node dragging, this also includes 'dragging' boolean.
                node_id = change["id"]
                node_idx = next((i for i, n in enumerate(self.nodes) if n["id"] == node_id), -1)
                if node_idx != -1:
                    if "position" in change:
                        self.nodes[node_idx]["position"] = change["position"]
                    if "positionAbsolute" in change: # For child nodes of a group
                        self.nodes[node_idx]["positionAbsolute"] = change["positionAbsolute"]
                    # if change.get("dragging") is False: self._save_version() # Save on drag end

            elif change["type"] == "remove": # Node removed by ReactFlow UI (e.g. backspace)
                node_id_to_remove = change["id"]
                self.nodes = [n for n in self.nodes if n["id"] != node_id_to_remove]
                self.edges = [e for e in self.edges if e["source"] != node_id_to_remove and e["target"] != node_id_to_remove]
                # self._save_version()


        # Update selected_nodes state based on aggregated selection changes
        if changes and any(c["type"] == "select" for c in changes):
            self.selected_nodes = new_selected_nodes_ids

        if len(self.selected_nodes) == 1:
            self.select_node(self.selected_nodes[0])
        elif not self.selected_nodes:
            self.deselect_node()
        # If multiple selected, selected_node might be the last one selected or cleared.
        # For multiple selections, UI should iterate selected_nodes.


    def select_node(self, node_id: Optional[str]):
        if node_id is None:
            self.deselect_node()
            return

        node_id_str = str(node_id)
        node = next((n for n in self.nodes if n["id"] == node_id_str), None)
        if node:
            self.selected_node = node
            # Ensure `selected_nodes` (plural) reflects this if not already handled by on_nodes_change
            if node_id_str not in self.selected_nodes:
                self.selected_nodes = [node_id_str] # Single selection replaces
        else:
            print(f"Node with ID {node_id_str} not found for selection.")
            self.selected_node = {}


    def deselect_node(self):
        self.selected_node = {}
        # `selected_nodes` (plural) should be cleared by on_nodes_change if pane is clicked
        # or if selection is programmatically cleared.
        # If deselect_node is called, assume all are deselected.
        # self.selected_nodes = []


    # AI Generation
    def generate_visual(self):
        # Placeholder: simulate image generation
        # In a real app, this would involve collecting data from connected nodes,
        # forming a prompt/payload, and calling an AI service.
        if not any(n["type"] == "input" for n in self.nodes):
            print("Generation requires at least one input node.")
            # self.show_toast("Error: Add an input node.", type="error")
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.preview_image = f"/placeholder/512/512.svg?text=Generated_{timestamp}"
        print(f"Simulating visual generation. Preview: {self.preview_image}")

        generation_details = {
            "id": f"gen_{timestamp}",
            "timestamp": datetime.datetime.now().isoformat(),
            "model_used": self.selected_model,
            "prompt_summary": "Workflow based generation", # TODO: Build from nodes
            "image_url": self.preview_image,
            "settings_snapshot": self.model_settings.copy(),
            "workflow_nodes_count": len(self.nodes),
        }
        self.generation_history.insert(0, generation_details) # Add to top
        if len(self.generation_history) > 20: # Limit history size
            self.generation_history = self.generation_history[:20]

        self.analytics["images_generated"] += 1
        self._save_version()


    def run_ab_test(self):
        # Find the A/B test node - assumes only one or the first one found.
        ab_test_node_id = None
        ab_node_data = None
        for node in self.nodes:
            if "a/b test" in node.get("data",{}).get("label","").lower():
                ab_test_node_id = node["id"]
                ab_node_data = node["data"]
                break
        
        if not ab_test_node_id or not ab_node_data:
            print("No A/B Test node found or selected to run.")
            # self.show_toast("Error: Add or select an A/B Test node.", type="error")
            return

        variants_count = ab_node_data.get("variants_count", 2)
        # test_parameter = ab_node_data.get("test_parameter", "style_name") # Example
        # test_values = ab_node_data.get("test_values", ["Vintage", "Cyberpunk"]) # Example

        results = []
        for i in range(variants_count):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            variant_image_url = f"/placeholder/300/300.svg?text=Variant_{chr(65+i)}_{timestamp}"
            result = {
                "variant_name": f"Variant {chr(65 + i)}",
                "image_url": variant_image_url,
                # "parameter_value_used": test_values[i] if i < len(test_values) else f"Value {i+1}",
                "score_mock": random.randint(60, 98),
                "engagement_mock": random.randint(500, 2000),
                "conversion_mock": round(random.uniform(1.5, 10.0), 1)
            }
            results.append(result)

        self.ab_test_results = results # Store results for the modal
        self.current_ab_test = { # Info about the test that was run
            "node_id": ab_test_node_id,
            # "parameter_tested": test_parameter,
            "results_summary": f"{variants_count} variants generated.",
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.analytics["ab_tests_run"] += 1
        
        # Update the A/B test node in self.nodes with its results
        for i, n in enumerate(self.nodes):
            if n["id"] == ab_test_node_id:
                self.nodes[i]["data"]["last_results"] = results # Store results in node data
                break
        
        self.show_ab_test_modal = True # Trigger modal visibility
        self._save_version()
        print(f"A/B Test run for node {ab_test_node_id}. Results generated.")

    # Template Management (Simplified from previous, focus on node/edge structure)
    def load_template(self, template_id: str):
        # Define templates directly here or load from a JSON/DB
        templates_data = {
            "social_media": {
                "nodes": [
                    {"id": "1", "type": "input", "data": {"label": "Your Image"}, "position": {"x": 50, "y": 50}},
                    {"id": "2", "type": "default", "data": {"label": "Brand Colors"}, "position": {"x": 250, "y": 50}},
                    {"id": "3", "type": "default", "data": {"label": "Post Text"}, "position": {"x": 50, "y": 200}},
                    {"id": "4", "type": "output", "data": {"label": "Social Post"}, "position": {"x": 450, "y": 125}},
                ],
                "edges": [
                    {"id": "e1-2", "source": "1", "target": "2"},
                    {"id": "e1-3", "source": "1", "target": "3"},
                    {"id": "e2-4", "source": "2", "target": "4"},
                    {"id": "e3-4", "source": "3", "target": "4"},
                ]
            },
             "logo_design": {
                "nodes": [
                    {"id": "1", "type": "default", "data": {"label": "Keywords Prompt"}, "position": {"x": 50, "y": 100}},
                    {"id": "2", "type": "default", "data": {"label": "Color Scheme"}, "position": {"x": 300, "y": 100}},
                    {"id": "3", "type": "output", "data": {"label": "Generated Logo"}, "position": {"x": 550, "y": 100}},
                ],
                "edges": [
                    {"id": "e1-2", "source": "1", "target": "2"},
                    {"id": "e2-3", "source": "2", "target": "3"},
                ]
            }
        }
        if template_id not in templates_data:
            print(f"Template '{template_id}' not found.")
            return

        template_content = templates_data[template_id]
        
        loaded_nodes = []
        for node_data in template_content["nodes"]:
            node_data_copy = json.loads(json.dumps(node_data)) # Deep copy
            # Ensure style is applied based on type
            if "style" not in node_data_copy:
                 node_data_copy["style"] = self._get_default_node_style(node_data_copy.get("type", "default"))
            loaded_nodes.append(node_data_copy)
        self.nodes = loaded_nodes

        loaded_edges = []
        for edge_data in template_content["edges"]:
            edge_data_copy = json.loads(json.dumps(edge_data)) # Deep copy
            if "animated" not in edge_data_copy: edge_data_copy["animated"] = True
            if "style" not in edge_data_copy: edge_data_copy["style"] = {"stroke": self.accent_color, "strokeWidth": 2}
            loaded_edges.append(edge_data_copy)
        self.edges = loaded_edges
        
        self.selected_template = template_id
        self._save_version()
        print(f"Template '{template_id}' loaded.")
        # Consider adding a call to fit the view in ReactFlow after loading

    # Project Management
    def save_project(self, project_name: str):
        if not project_name.strip():
            print("Project name cannot be empty.")
            return
        
        project_id = f"proj_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        project_data = {
            "id": project_id,
            "name": project_name,
            "nodes": json.loads(json.dumps(self.nodes)), # Deep copy for saving
            "edges": json.loads(json.dumps(self.edges)),
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(), # Same as created for new save
            "preview_image": self.preview_image,
            "canvas_state_snapshot": { # Optionally save some key state vars
                "selected_model": self.selected_model,
                "model_settings": self.model_settings.copy(),
                "current_style": self.current_style,
                "zoom_level": self.zoom_level,
            }
        }
        self.saved_projects.insert(0, project_data) # Add to top
        if len(self.saved_projects) > 10: # Limit number of saved projects in memory
            self.saved_projects = self.saved_projects[:10]
        
        self.show_save_dialog = False # Close dialog
        print(f"Project '{project_name}' saved with ID {project_id}.")

    def load_project(self, project_id: str):
        project_to_load = next((p for p in self.saved_projects if p["id"] == project_id), None)
        if not project_to_load:
            print(f"Project with ID '{project_id}' not found.")
            return

        self.nodes = json.loads(json.dumps(project_to_load["nodes"]))
        self.edges = json.loads(json.dumps(project_to_load["edges"]))
        self.preview_image = project_to_load.get("preview_image", "")
        
        snapshot = project_to_load.get("canvas_state_snapshot", {})
        self.selected_model = snapshot.get("selected_model", self.selected_model)
        self.model_settings = snapshot.get("model_settings", self.model_settings)
        self.current_style = snapshot.get("current_style", self.current_style)
        self.zoom_level = snapshot.get("zoom_level", self.zoom_level)
        
        # Reset selection state
        self.selected_node = {}
        self.selected_nodes = []
        
        self.show_load_dialog = False # Close dialog
        self._save_version() # Create a new version upon loading a project
        print(f"Project '{project_to_load['name']}' loaded.")


    # Version Control
    def _save_version(self):
        if not self.auto_save_enabled:
            return
        
        # More robust check for meaningful change before saving a version
        current_snapshot = {"nodes": self.nodes, "edges": self.edges}
        if self.version_history:
            last_version_snapshot = {"nodes": self.version_history[-1]["nodes"], "edges": self.version_history[-1]["edges"]}
            # Basic check, could be improved with deep comparison or hashing
            if json.dumps(current_snapshot, sort_keys=True) == json.dumps(last_version_snapshot, sort_keys=True):
                return # No change, don't save duplicate version

        self.current_version += 1
        version_data = {
            "version": self.current_version,
            "timestamp": datetime.datetime.now().isoformat(),
            "nodes": json.loads(json.dumps(self.nodes)), # Deep copy
            "edges": json.loads(json.dumps(self.edges)),
            "description": f"Version {self.current_version}"
        }
        self.version_history.append(version_data)
        
        # Limit history size
        max_history = 50
        if len(self.version_history) > max_history:
            self.version_history = self.version_history[-max_history:]
        print(f"Saved version {self.current_version}.")


    def restore_version(self, version_number: int):
        version_to_restore = next((v for v in self.version_history if v["version"] == version_number), None)
        if not version_to_restore:
            print(f"Version {version_number} not found in history.")
            return

        self.nodes = json.loads(json.dumps(version_to_restore["nodes"]))
        self.edges = json.loads(json.dumps(version_to_restore["edges"]))
        # current_version should reflect the restored version number
        # self.current_version = version_number # Or keep incrementing for new changes
        print(f"Restored to state of version {version_number}.")
        # Do not call _save_version here, as that would create a new version identical to the restored one.
        # User should make a change for a new version to be saved.


    # Export (Simulation)
    def export_canvas(self):
        print(f"Exporting canvas: Format={self.selected_export_format}, Size={self.selected_export_size}, Quality={self.render_quality}")
        if self.selected_export_size == "Custom":
            print(f"Custom: {self.custom_width}x{self.custom_height}")
        self.analytics["exports_made"] += 1
        self.show_export_modal = False


    # Settings & Preferences
    def update_model_settings(self, setting: str, value: Any):
        if setting in self.model_settings:
            self.model_settings[setting] = value
            print(f"Model setting '{setting}' updated to {value}.")
        else:
            print(f"Warning: Attempt to set unknown model setting '{setting}'.")

    def set_theme(self, theme_name: str): # For Radix theme
        if theme_name in ["light", "dark"]:
            self.theme = theme_name
            # This would trigger reflex_app.theme update or a Theme component re-render
            print(f"App theme set to: {theme_name}. Requires Radix ThemeProvider update.")
        else:
            print(f"Invalid theme name: {theme_name}")


    def set_accent_color(self, color: str): # For Radix theme
        self.accent_color = color
        print(f"App accent color set to: {color}. Requires Radix ThemeProvider update.")

    # Other toggles...
    def toggle_auto_save(self): self.auto_save_enabled = not self.auto_save_enabled
    def toggle_grid(self): self.grid_enabled = not self.grid_enabled
    def toggle_snap_to_grid(self): self.snap_to_grid = not self.snap_to_grid # Needs RF prop
    def toggle_rulers(self): self.rulers_enabled = not self.rulers_enabled
    def set_zoom_level(self, zoom: float): self.zoom_level = max(0.1, min(5.0, zoom)) # Needs RF prop
    def set_render_quality(self, quality: str): self.render_quality = quality
    def toggle_real_time_preview(self): self.real_time_preview = not self.real_time_preview


    # Tutorial System Methods (Simplified)
    def start_tutorial(self, tutorial_type: str = "basic"):
        self.tutorial_active = True
        self.tutorial_type = tutorial_type
        self.tutorial_step = 0 # Start from step 0 (first step)
        self.show_tutorial = True
        print(f"Tutorial '{tutorial_type}' started.")

    def next_tutorial_step(self):
        # Define tutorial steps content somewhere, e.g., a list of dicts
        tutorial_steps_count = {"basic": 3, "advanced": 5}.get(self.tutorial_type, 3)
        if self.tutorial_step < tutorial_steps_count - 1:
            self.tutorial_step += 1
        else:
            self.end_tutorial() # End if last step

    def prev_tutorial_step(self):
        if self.tutorial_step > 0:
            self.tutorial_step -= 1

    def end_tutorial(self):
        self.tutorial_active = False
        self.show_tutorial = False
        self.tutorial_step = 0 # Reset
        print("Tutorial ended.")


    # Collaboration (Placeholders - needs backend and real-time sync)
    def invite_collaborator(self, email: str, role: str = "editor"):
        print(f"Placeholder: Inviting {email} as {role}.")
    def update_collaborator_role(self, collab_id: str, new_role: str):
        print(f"Placeholder: Updating role for {collab_id} to {new_role}.")
    def remove_collaborator(self, collab_id: str):
        print(f"Placeholder: Removing collaborator {collab_id}.")


    # Advanced AI (Placeholders)
    def generate_prompt_suggestions(self, context: str = "") -> List[str]:
        # This should return a list of strings
        return [
            "A serene landscape at dusk", "Cyberpunk city street", "Vintage portrait photography",
            "Abstract geometric patterns in gold and teal", "Product shot for a luxury watch"
        ][:3] # Return a few

    def auto_optimize_workflow(self) -> List[Dict[str, str]]:
        # Placeholder for workflow analysis
        suggestions = []
        if len(self.nodes) > 10 and not self.edges:
            suggestions.append({"type": "connection_needed", "message": "Many nodes but no connections. Connect nodes to form a workflow."})
        if not any(n["type"] == "output" for n in self.nodes) and self.nodes:
            suggestions.append({"type": "output_missing", "message": "No output node found. Add an output node to define the final result."})
        return suggestions


    # Performance Analytics (Placeholders)
    def get_performance_metrics(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "workflow_complexity": self._calculate_complexity(),
            "avg_generation_time_sec": "N/A", # Would come from actual measurements
            "optimization_score": self._calculate_optimization_score(),
        }

    def _calculate_complexity(self) -> str:
        score = len(self.nodes) + len(self.edges) * 1.5
        if score < 5: return "Low"
        if score < 15: return "Medium"
        if score < 30: return "High"
        return "Very High"

    def _calculate_optimization_score(self) -> int:
        # Basic mock score
        score = 80
        if not any(n["type"] == "output" for n in self.nodes) and self.nodes: score -= 20
        if not self.edges and len(self.nodes) > 1 : score -= 10
        return max(0, min(100, score))
