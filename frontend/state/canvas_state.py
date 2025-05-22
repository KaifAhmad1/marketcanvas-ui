# frontend/state/canvas_state.py
import reflex as rx
from typing import Any, Dict, List, Optional
import random
import json
import datetime
import aiohttp
import asyncio

initial_nodes = [
    {
        "id": "1",
        "type": "input",
        "data": {"label": "Base Image", "image_url": "", "filters": [], "brightness": 100, "contrast": 100, "status": "idle"},
        "position": {"x": 100, "y": 50},
        "style": {"background": "#1e40af", "color": "white", "border": "2px solid #3b82f6", "borderRadius": "12px"}
    },
    {
        "id": "2",
        "type": "default",
        "data": {"label": "Style Node", "style": "Modern", "intensity": 0.7, "color_palette": ["#3b82f6", "#8b5cf6"], "status": "idle"},
        "position": {"x": 300, "y": 125},
        "style": {"background": "#7c3aed", "color": "white", "border": "2px solid #a855f7", "borderRadius": "12px"}
    },
    {
        "id": "3",
        "type": "output",
        "data": {"label": "AI Generator", "model": "DALL-E 3", "prompt": "", "steps": 50, "status": "idle"},
        "position": {"x": 500, "y": 100},
        "style": {"background": "#059669", "color": "white", "border": "2px solid #10b981", "borderRadius": "12px"}
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2", "animated": True, "style": {"stroke": "#3b82f6", "strokeWidth": 2}, "type": "image"},
    {"id": "e2-3", "source": "2", "target": "3", "animated": True, "style": {"stroke": "#8b5cf6", "strokeWidth": 2}, "type": "style"},
]

class CanvasState(rx.State):
    # Canvas Data
    nodes: List[Dict[str, Any]] = initial_nodes
    edges: List[Dict[str, Any]] = initial_edges
    selected_node: Dict[str, Any] = {}
    selected_nodes: List[str] = []
    group_collapsed_ids: List[str] = []

    # Preview & Generation
    preview_image: str = ""
    generated_images: List[Dict[str, Any]] = []
    generation_history: List[Dict[str, Any]] = []

    # UI States
    show_context_menu: bool = False
    show_tutorial: bool = False
    show_settings: bool = False
    show_export_modal: bool = False
    show_save_dialog: bool = False
    show_load_dialog: bool = False
    show_collaboration_panel: bool = False
    show_properties_panel: bool = True
    show_layers_panel: bool = True
    show_ab_test_modal: bool = False
    show_tutorial_spotlight: bool = False
    spotlight_position: Dict[str, float] = {"x": 0, "y": 0}
    spotlight_size: Dict[str, float] = {"width": 100, "height": 100}
    canvas_theme: str = "grid"

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
        "time_spent": 0
    }

    # A/B Testing
    ab_test_results: List[Dict[str, Any]] = []
    current_ab_test: Dict[str, Any] = {}

    # Templates & Projects
    saved_projects: List[Dict[str, Any]] = []
    templates: List[Dict[str, Any]] = [
        {"id": "social_media", "name": "Social Media Post", "category": "Social", "preview": "/placeholder/400/400.svg?text=Social"},
        {"id": "banner_ad", "name": "Banner Ad", "category": "Advertising", "preview": "/placeholder/728/90.svg?text=Banner"},
        {"id": "logo_design", "name": "Logo Design", "category": "Branding", "preview": "/placeholder/300/300.svg?text=Logo"},
    ]
    selected_template: str = ""
    active_settings_tab: str = "general"

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
        "seed": -1,
        "batch_size": 1
    }

    # Collaboration
    collaborators: List[Dict[str, Any]] = []
    current_user: Dict[str, str] = {"id": "user_default_1", "name": "Default User", "role": "owner", "avatar": "/placeholder/40/40.svg?text=U"}
    project_permissions: Dict[str, bool] = {"can_edit": True, "can_export": True, "can_share": True}

    # Text & Overlays
    text_overlays: List[Dict[str, Any]] = []
    selected_overlay: Optional[int] = None

    # Filters & Effects
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
    current_version: int = 0
    auto_save_enabled: bool = True
    grid_enabled: bool = True
    snap_to_grid: bool = True
    rulers_enabled: bool = False
    zoom_level: float = 1.0
    render_quality: str = "High"
    real_time_preview: bool = True
    gpu_acceleration: bool = True

    # API Key
    api_key: str = ""

    @rx.var
    def has_saved_projects(self) -> bool:
        return len(self.saved_projects) > 0

    @rx.var
    def accent_color(self) -> str:
        theme_colors = {
            "grid": "#3b82f6",
            "dots": "#8b5cf6",
            "gradient": "#d946ef"
        }
        return theme_colors.get(self.canvas_theme, "#3b82f6")

    def toggle_canvas_theme(self):
        themes = ["grid", "dots", "gradient"]
        current_idx = themes.index(self.canvas_theme) if self.canvas_theme in themes else 0
        self.canvas_theme = themes[(current_idx + 1) % len(themes)]

    def toggle_grid(self):
        self.grid_enabled = not self.grid_enabled

    def toggle_rulers(self):
        self.rulers_enabled = not self.rulers_enabled

    def set_zoom_level(self, level: float):
        self.zoom_level = max(0.2, min(4.0, level))

    def _create_node_id(self) -> str:
        max_id = 0
        for node in self.nodes:
            try:
                node_id_int = int(node["id"])
                if node_id_int > max_id:
                    max_id = node_id_int
            except ValueError:
                pass
        return str(max_id + 1)

    def _get_default_node_style(self, node_type: str) -> Dict[str, str]:
        base_style = {"color": "white", "borderRadius": "12px"}
        type_styles = {
            "input": {"background": "#1D4ED8", "border": "2px solid #3B82F6"},
            "output": {"background": "#059669", "border": "2px solid #10B981"},
            "default": {"background": "#7C3AED", "border": "2px solid #A78BFA"},
            "text": {"background": "#D97706", "border": "2px solid #F59E0B"},
            "ai_processor": {"background": "#DC2626", "border": "2px solid #EF4444"},
            "ab_test": {"background": "#EA580C", "border": "2px solid #F97316"},
            "annotation": {"background": "#6B7280", "border": "2px solid #9CA3AF"},
            "group": {"backgroundColor": "rgba(107, 114, 128, 0.1)", "border": "1px dashed #9CA3AF"}
        }
        return {**base_style, **type_styles.get(node_type, type_styles["default"])}

    def get_node_icon(self, node_type: str) -> str:
        icon_map = {
            "input": "image",
            "output": "arrow-down-to-line",
            "default": "circle",
            "text": "type",
            "ai_processor": "cpu",
            "ab_test": "git-fork",
            "annotation": "pen-square",
            "group": "folder"
        }
        return icon_map.get(node_type, "circle")

    def add_node_by_type(self, node_type_str: str, data: Optional[Dict[str, Any]] = None):
        new_node_id = self._create_node_id()
        base_data = {"label": f"{node_type_str.replace('_', ' ').title()} Node", "status": "idle"}
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
            "annotation": {"type": "default", "data": {"label": "Annotation", "text": "Note", "font_size": 16}},
        }

        config = node_config.get(node_type_str, {"type": "default", "data": {"label": "Custom Node"}})
        final_data = config["data"].copy()
        if data: 
            final_data.update(data)

        new_node = {
            "id": new_node_id,
            "type": config["type"],
            "data": final_data,
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": self._get_default_node_style(node_type_str)
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()
        self.show_toast(f"Added {node_type_str.title()} node", type="success")

    def add_base_image_node(self): self.add_node_by_type("input")
    def add_style_node(self): self.add_node_by_type("style")
    def add_ai_processor_node(self): self.add_node_by_type("ai_processor")
    def add_text_node(self): self.add_node_by_type("text")
    def add_filter_node(self): self.add_node_by_type("filter")
    def add_ab_test_node(self): self.add_node_by_type("ab_test")
    def add_output_node(self): self.add_node_by_type("output")
    def add_annotation_node(self): self.add_node_by_type("annotation")

    def clear_canvas(self):
        self.nodes = []
        self.edges = []
        self.selected_node = {}
        self.selected_nodes = []
        self.preview_image = ""
        self.text_overlays = []
        self.group_collapsed_ids = []
        self._save_version()
        self.show_toast("Canvas cleared", type="info")

    def duplicate_selected_nodes(self):
        if not self.selected_nodes:
            self.show_toast("No nodes selected to duplicate", type="warning")
            return
        newly_added_nodes = []
        for node_id_str in self.selected_nodes:
            original_node = next((n for n in self.nodes if n["id"] == node_id_str), None)
            if original_node:
                new_node_id = self._create_node_id()
                new_data = json.loads(json.dumps(original_node["data"]))
                new_node = {
                    "id": new_node_id,
                    "type": original_node["type"],
                    "data": new_data,
                    "position": {
                        "x": original_node["position"]["x"] + 40,
                        "y": original_node["position"]["y"] + 40
                    },
                    "style": original_node.get("style", {}).copy()
                }
                newly_added_nodes.append(new_node)
        if newly_added_nodes:
            self.nodes.extend(newly_added_nodes)
            self.analytics["nodes_created"] += len(newly_added_nodes)
            self._save_version()
            self.selected_nodes = [n["id"] for n in newly_added_nodes]
            if len(self.selected_nodes) == 1:
                self.select_node(self.selected_nodes[0])
            self.show_toast(f"Duplicated {len(newly_added_nodes)} node(s)", type="success")

    def delete_selected_nodes(self):
        if not self.selected_nodes:
            self.show_toast("No nodes selected to delete", type="warning")
            return
        
        ids_to_delete_str = set(self.selected_nodes)
        original_node_count = len(self.nodes)
        self.nodes = [n for n in self.nodes if n["id"] not in ids_to_delete_str]
        deleted_count = original_node_count - len(self.nodes)
        self.edges = [e for e in self.edges if e["source"] not in ids_to_delete_str and e["target"] not in ids_to_delete_str]
        self.selected_nodes = []
        self.selected_node = {}
        self.group_collapsed_ids = [gid for gid in self.group_collapsed_ids if gid not in ids_to_delete_str]
        if deleted_count > 0:
            self._save_version()
            self.show_toast(f"Deleted {deleted_count} node(s)", type="success")

    def group_selected_nodes(self):
        if len(self.selected_nodes) <= 1:
            self.show_toast("Select more than one node to group", type="warning")
            return

        group_id = f"group_{self._create_node_id()}"
        children_ids = [str(nid) for nid in self.selected_nodes]
        group_bounds = self._calculate_group_bounds(children_ids)

        group_node = {
            "id": group_id,
            "type": "group",
            "data": {
                "label": f"Group ({len(children_ids)} nodes)",
            },
            "position": group_bounds["position"],
            "style": {
                "backgroundColor": "rgba(107, 114, 128, 0.1)",
                "borderColor": "rgb(156, 163, 175)",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "8px",
                "width": group_bounds["width"],
                "height": group_bounds["height"],
            },
        }
        
        updated_nodes = []
        group_x, group_y = group_node["position"]["x"], group_node["position"]["y"]
        for node in self.nodes:
            if node["id"] in children_ids:
                node["parentNode"] = group_id
                node["extent"] = "parent"
            updated_nodes.append(node)
        
        self.nodes = updated_nodes
        self.nodes.append(group_node)
        self.selected_nodes = [group_id]
        self.select_node(group_id)
        self._save_version()
        self.show_toast(f"Grouped {len(children_ids)} nodes", type="success")

    def ungroup_selected_nodes(self):
        if not self.selected_nodes:
            self.show_toast("No nodes selected to ungroup", type="warning")
            return

        group_id = self.selected_nodes[0]
        group_node = next((n for n in self.nodes if n["id"] == group_id and n["type"] == "group"), None)
        if not group_node:
            self.show_toast("Selected node is not a group", type="warning")
            return

        updated_nodes = []
        for node in self.nodes:
            if node.get("parentNode") == group_id:
                node_copy = node.copy()
                del node_copy["parentNode"]
                del node_copy["extent"]
                updated_nodes.append(node_copy)
            elif node["id"] != group_id:
                updated_nodes.append(node)

        self.nodes = updated_nodes
        self.group_collapsed_ids = [gid for gid in self.group_collapsed_ids if gid != group_id]
        self.selected_nodes = []
        self.selected_node = {}
        self._save_version()
        self.show_toast(f"Ungrouped nodes", type="success")

    def toggle_group_collapse(self, group_id: str):
        if group_id in self.group_collapsed_ids:
            self.group_collapsed_ids.remove(group_id)
        else:
            self.group_collapsed_ids.append(group_id)
        self._save_version()

    def _calculate_group_bounds(self, node_ids: List[str]) -> Dict[str, Any]:
        selected_node_objects = [n for n in self.nodes if n["id"] in node_ids]
        if not selected_node_objects:
            return {"position": {"x": 0, "y": 0}, "width": 200, "height": 100}

        get_node_width = lambda node: node.get("width", 150)
        get_node_height = lambda node: node.get("height", 50)

        min_x = min(n["position"]["x"] for n in selected_node_objects)
        min_y = min(n["position"]["y"] for n in selected_node_objects)
        max_x = max(n["position"]["x"] + get_node_width(n) for n in selected_node_objects)
        max_y = max(n["position"]["y"] + get_node_height(n) for n in selected_node_objects)

        padding = 30
        return {
            "position": {"x": min_x - padding, "y": min_y - padding},
            "width": (max_x - min_x) + (2 * padding),
            "height": (max_y - min_y) + (2 * padding)
        }

    def on_connect(self, connection: Dict[str, str]):
        source_id = connection.get("source")
        target_id = connection.get("target")
        source_handle = connection.get("sourceHandle")
        target_handle = connection.get("targetHandle")

        if not source_id or not target_id:
            self.show_toast("Invalid connection", type="error")
            return

        if source_id == target_id:
            self.show_toast("Self-loops are not allowed", type="error")
            return

        new_edge_id = f"e_{source_id}{source_handle or ''}-{target_id}{target_handle or ''}"
        if any(e["id"] == new_edge_id for e in self.edges):
            self.show_toast("Edge already exists", type="warning")
            return

        new_edge = {
            "id": new_edge_id,
            "source": source_id,
            "target": target_id,
            "sourceHandle": source_handle,
            "targetHandle": target_handle,
            "animated": True,
            "style": {"stroke": self.accent_color, "strokeWidth": 2},
            "label": self._get_edge_label(source_id, target_id),
            "type": self._get_edge_type(source_id, target_id)
        }
        self.edges.append(new_edge)
        self._save_version()
        self.show_toast("Edge created", type="success")

    def _get_edge_label(self, source_id: str, target_id: str) -> str:
        source_node = next((n for n in self.nodes if n["id"] == source_id), None)
        if source_node:
            label_lower = source_node.get("data", {}).get("label", "").lower()
            if source_node.get("type") == "input": return "Image Data"
            if "style" in label_lower: return "Apply Style"
            if "filter" in label_lower: return "Apply Filter"
            if "text" in label_lower: return "Text Overlay"
            if "annotation" in label_lower: return "Annotation"
        return "Connects"

    def _get_edge_type(self, source_id: str, target_id: str) -> str:
        source_node = next((n for n in self.nodes if n["id"] == source_id), None)
        if source_node:
            label_lower = source_node.get("data", {}).get("label", "").lower()
            if "image" in label_lower: return "image"
            if "text" in label_lower: return "text"
            if "style" in label_lower: return "style"
        return "default"

    def on_nodes_change(self, changes: List[Dict[str, Any]]):
        new_selected_nodes_ids = []
        for change in changes:
            if change["type"] == "select":
                node_id = change["id"]
                if change["selected"]:
                    new_selected_nodes_ids.append(node_id)
            elif change["type"] == "position":
                node_id = change["id"]
                node_idx = next((i for i, n in enumerate(self.nodes) if n["id"] == node_id), -1)
                if node_idx != -1:
                    if "position" in change:
                        self.nodes[node_idx]["position"] = change["position"]
                    if "positionAbsolute" in change:
                        self.nodes[node_idx]["positionAbsolute"] = change["positionAbsolute"]
            elif change["type"] == "remove":
                node_id_to_remove = change["id"]
                self.nodes = [n for n in self.nodes if n["id"] != node_id_to_remove]
                self.edges = [e for e in self.edges if e["source"] != node_id_to_remove and e["target"] != node_id_to_remove]

        if changes and any(c["type"] == "select" for c in changes):
            self.selected_nodes = new_selected_nodes_ids

        if len(self.selected_nodes) == 1:
            self.select_node(self.selected_nodes[0])
        elif not self.selected_nodes:
            self.deselect_node()

    def select_node(self, node_id: Optional[str]):
        if node_id is None:
            self.deselect_node()
            return

        node_id_str = str(node_id)
        node = next((n for n in self.nodes if n["id"] == node_id_str), None)
        if node:
            self.selected_node = node
            if node_id_str not in self.selected_nodes:
                self.selected_nodes = [node_id_str]
        else:
            self.selected_node = {}
            self.show_toast(f"Node {node_id_str} not found", type="error")

    def deselect_node(self):
        self.selected_node = {}
        self.selected_nodes = []

    def update_node_property(self, node_id: str, field: str, value: Any):
        for i, node in enumerate(self.nodes):
            if node["id"] == node_id:
                fields = field.split(".")
                target = node
                for f in fields[:-1]:
                    target = target.setdefault(f, {})
                target[fields[-1]] = value
                self.nodes[i] = node
                if node_id == self.selected_node.get("id"):
                    self.selected_node = node
                self._save_version()
                break

    async def generate_visual(self):
        if not any(n["type"] == "input" for n in self.nodes):
            self.show_toast("Error: Add an input node", type="error")
            return

        for i, node in enumerate(self.nodes):
            self.nodes[i]["data"]["status"] = "processing"

        # Prepare workflow data
        workflow_data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "model_id": self.selected_model,
            "settings": self.model_settings
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:8000/api/canvas/generate",
                    json=workflow_data,
                    headers={"X-API-Key": self.api_key}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"API error: {await response.text()}")
                    result = await response.json()
                    self.preview_image = result.get("image_url", "/placeholder/512/512.svg")
        except Exception as e:
            self.show_toast(f"Generation failed: {str(e)}", type="error")
            for i, node in enumerate(self.nodes):
                self.nodes[i]["data"]["status"] = "error"
            return

        generation_details = {
            "id": f"gen_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.datetime.now().isoformat(),
            "image_url": self.preview_image,
            "settings": self.model_settings.copy(),
            "model_id": self.selected_model
        }
        self.generated_images.append(generation_details)
        self.generation_history.append(generation_details)
        self.analytics["images_generated"] += 1

        for i, node in enumerate(self.nodes):
            self.nodes[i]["data"]["status"] = "complete"
        
        self._save_version()
        self.show_toast("Image generated successfully", type="success")

    def generate_prompt_suggestions(self) -> List[str]:
        base_prompts = [
            "A vibrant social media banner with bold typography",
            "A minimalist logo with geometric shapes",
            "A retro-style poster with vibrant colors",
            "A modern website hero image with abstract elements",
            "A product advertisement with sleek design"
        ]
        return base_prompts

    def apply_suggestion(self, suggestion: str):
        for i, node in enumerate(self.nodes):
            if node.get("data", {}).get("label", "").lower().contains("ai generator"):
                self.nodes[i]["data"]["prompt"] = suggestion
                if node["id"] == self.selected_node.get("id"):
                    self.selected_node["data"]["prompt"] = suggestion
                self._save_version()
                self.show_toast("Applied suggestion to AI node", type="success")
                break
        else:
            self.show_toast("No AI Generator node found", type="warning")

    def auto_optimize_workflow(self) -> List[Dict[str, str]]:
        suggestions = []
        node_types = [n.get("type") for n in self.nodes]
        edge_count = len(self.edges)

        if "input" not in node_types:
            suggestions.append({"message": "Add an Input node to start your workflow"})
        if edge_count == 0 and len(self.nodes) > 1:
            suggestions.append({"message": "Connect nodes to create a workflow"})
        if any(n.get("data", {}).get("prompt", "") == "" for n in self.nodes if n.get("data", {}).get("label", "").lower().contains("ai generator")):
            suggestions.append({"message": "Add a prompt to your AI Generator node"})
        if len(self.nodes) > 5 and "group" not in node_types:
            suggestions.append({"message": "Consider grouping related nodes for better organization"})

        return suggestions

    def update_model_settings(self, key: str, value: Any):
        self.model_settings[key] = value
        self._save_version()

    def start_layer_manipulation(self):
        self.show_toast("Layer manipulation started (drag to adjust)", type="info")

    def edit_preview_text(self):
        for i, node in enumerate(self.nodes):
            if node.get("data", {}).get("label", "").lower().contains("text overlay"):
                self.select_node(node["id"])
                self.show_toast("Selected text node for editing", type="info")
                return
        self.show_toast("No text overlay node found", type="warning")

    def export_canvas(self):
        export_data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "format": self.selected_export_format,
            "size": self.selected_export_size,
            "custom_width": self.custom_width if self.selected_export_size == "Custom" else None,
            "custom_height": self.custom_height if self.selected_export_size == "Custom" else None
        }
        self.analytics["exports_made"] += 1
        self.show_toast(f"Exported canvas as {self.selected_export_format}", type="success")
        self.show_export_modal = False
        self._save_version()

    def load_project(self, project_id: str):
        project = next((p for p in self.saved_projects if p["id"] == project_id), None)
        if project:
            self.nodes = project.get("nodes", [])
            self.edges = project.get("edges", [])
            self.preview_image = project.get("preview_image", "")
            self.show_toast(f"Loaded project: {project.get('name', 'Untitled')}", type="success")
            self._save_version()
            rx.redirect("/editor")
        else:
            self.show_toast("Project not found", type="error")

    def save_project(self, project_name: str = "Untitled"):
        project_id = f"proj_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        project = {
            "id": project_id,
            "name": project_name,
            "nodes": self.nodes,
            "edges": self.edges,
            "preview_image": self.preview_image,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }
        self.saved_projects.append(project)
        self.show_toast(f"Saved project: {project_name}", type="success")
        self._save_version()

    def _save_version(self):
        if not self.auto_save_enabled:
            return
        version_data = {
            "nodes": json.loads(json.dumps(self.nodes)),
            "edges": json.loads(json.dumps(self.edges)),
            "preview_image": self.preview_image,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.version_history = self.version_history[:self.current_version + 1]
        self.version_history.append(version_data)
        self.current_version = len(self.version_history) - 1
        if len(self.version_history) > 50:
            self.version_history.pop(0)
            self.current_version -= 1

    def undo(self):
        if self.current_version > 0:
            self.current_version -= 1
            version = self.version_history[self.current_version]
            self.nodes = version["nodes"]
            self.edges = version["edges"]
            self.preview_image = version["preview_image"]
            self.show_toast("Undo successful", type="info")

    def redo(self):
        if self.current_version < len(self.version_history) - 1:
            self.current_version += 1
            version = self.version_history[self.current_version]
            self.nodes = version["nodes"]
            self.edges = version["edges"]
            self.preview_image = version["preview_image"]
            self.show_toast("Redo successful", type="info")

    def start_tutorial(self):
        self.show_tutorial = True
        self.tutorial_step = 0
        self.tutorial_active = True
        self.show_tutorial_spotlight = True
        self.update_spotlight_position()

    def next_tutorial_step(self):
        self.tutorial_step += 1
        if self.tutorial_step >= 5:
            self.end_tutorial()
        else:
            self.update_spotlight_position()

    def prev_tutorial_step(self):
        if self.tutorial_step > 0:
            self.tutorial_step -= 1
            self.update_spotlight_position()

    def end_tutorial(self):
        self.show_tutorial = False
        self.tutorial_active = False
        self.show_tutorial_spotlight = False
        self.tutorial_step = 0
        self.show_toast("Tutorial completed!", type="success")

    def update_spotlight_position(self):
        step_positions = [
            {"x": 20, "y": 20, "width": 150, "height": 40},  # Toolbar: Base Image
            {"x": 170, "y": 20, "width": 150, "height": 40}, # Toolbar: Style
            {"x": 320, "y": 20, "width": 150, "height": 40}, # Toolbar: AI Gen
            {"x": 470, "y": 20, "width": 150, "height": 40}, # Toolbar: Text/Filter
            {"x": 1500, "y": 20, "width": 300, "height": 200} # Preview Panel (adjusted for typical screen width)
        ]
        if self.tutorial_step < len(step_positions):
            self.spotlight_size = step_positions[self.tutorial_step]
        else:
            self.show_tutorial_spotlight = False

    def show_toast(self, message: str, type: str = "info"):
        # Note: Reflex doesn't have a built-in toast component, so we simulate it
        # The UI component `toast_notification` will handle the visual display
        pass  # Handled by ui_components.py rendering

    def run_ab_test(self):
        if not any(n.get("data", {}).get("label", "").lower().contains("a/b test") for n in self.nodes):
            self.show_toast("Add an A/B Test node first", type="warning")
            return

        self.ab_test_results = [
            {"variant_name": "Variant A", "image_url": "/placeholder/100/100.svg", "score_mock": 85, "engagement_mock": 120},
            {"variant_name": "Variant B", "image_url": "/placeholder/100/100.svg", "score_mock": 78, "engagement_mock": 95}
        ]
        self.analytics["ab_tests_run"] += 1
        self.show_ab_test_modal = True
        self.show_toast("A/B Test completed", type="success")
        self._save_version()
