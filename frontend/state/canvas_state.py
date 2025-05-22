import reflex as rx
from typing import Any, Dict, List, Optional
import random
import json
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
    selected_node: Dict[str, Any] = {}
    selected_nodes: List[str] = []
    
    # Preview & Generation
    preview_image: str = ""
    generated_images: List[Dict[str, Any]] = []
    generation_history: List[Dict[str, Any]] = []
    
    # Styles & Themes
    current_style: str = "Modern"
    current_tone: str = "Professional"
    available_styles: List[str] = ["Modern", "Vintage", "Minimalist", "Luxury", "Cyberpunk", "Artistic", "Corporate", "Playful"]
    available_tones: List[str] = ["Professional", "Casual", "Elegant", "Bold", "Friendly", "Mysterious", "Energetic", "Calm"]
    theme: str = "dark"
    accent_color: str = "#3b82f6"
    theme_background: str = "#1f2937"
    custom_themes: Dict[str, Dict[str, str]] = {}
    
    # UI States
    show_context_menu: bool = False
    show_tutorial: bool = False
    show_settings: bool = False
    show_export_modal: bool = False
    show_save_dialog: bool = False
    show_load_dialog: bool = False
    show_collaboration_panel: bool = False
    
    # Tutorial System
    tutorial_step: int = 0
    tutorial_active: bool = False
    tutorial_type: str = "basic"  # basic, advanced, expert
    
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
        {"id": "social_media", "name": "Social Media Post", "category": "Social", "preview": "/api/placeholder/400/400"},
        {"id": "banner_ad", "name": "Banner Ad", "category": "Advertising", "preview": "/api/placeholder/728/90"},
        {"id": "logo_design", "name": "Logo Design", "category": "Branding", "preview": "/api/placeholder/300/300"},
        {"id": "business_card", "name": "Business Card", "category": "Print", "preview": "/api/placeholder/350/200"},
        {"id": "poster", "name": "Event Poster", "category": "Print", "preview": "/api/placeholder/400/600"},
        {"id": "newsletter", "name": "Newsletter", "category": "Email", "preview": "/api/placeholder/600/800"},
    ]
    selected_template: str = ""
    
    # AI Models & Settings
    available_models: List[Dict[str, Any]] = [
        {"id": "dalle3", "name": "DALL-E 3", "provider": "OpenAI", "speed": "Medium", "quality": "High"},
        {"id": "midjourney", "name": "Midjourney", "provider": "Midjourney", "speed": "Slow", "quality": "Excellent"},
        {"id": "stable_diffusion", "name": "Stable Diffusion XL", "provider": "Stability AI", "speed": "Fast", "quality": "Good"},
        {"id": "firefly", "name": "Adobe Firefly", "provider": "Adobe", "speed": "Medium", "quality": "High"},
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
    current_user: Dict[str, str] = {"id": "user1", "name": "You", "role": "owner", "avatar": "/api/placeholder/40/40"}
    project_permissions: Dict[str, bool] = {"can_edit": True, "can_export": True, "can_share": True}
    
    # Text & Overlays
    text_overlays: List[Dict[str, Any]] = []
    selected_overlay: Optional[int] = None
    
    # Filters & Effects
    available_filters: List[str] = ["None", "Blur", "Sharpen", "Vintage", "Black & White", "Sepia", "Vignette", "HDR"]
    available_effects: List[str] = ["None", "Drop Shadow", "Glow", "Emboss", "3D", "Neon", "Glitch", "Oil Paint"]
    
    # Export Settings
    export_formats: List[str] = ["PNG", "JPG", "SVG", "PDF", "GIF"]
    export_sizes: List[str] = ["Original", "Instagram (1080x1080)", "Facebook (1200x630)", "Twitter (1200x675)", "Custom"]
    selected_export_format: str = "PNG"
    selected_export_size: str = "Original"
    custom_width: int = 1920
    custom_height: int = 1080
    
    # Advanced Features
    version_history: List[Dict[str, Any]] = []
    current_version: int = 1
    auto_save_enabled: bool = True
    grid_enabled: bool = True
    snap_to_grid: bool = True
    rulers_enabled: bool = False
    zoom_level: float = 1.0
    
    # Performance & Quality
    render_quality: str = "High"  # Low, Medium, High, Ultra
    real_time_preview: bool = True
    gpu_acceleration: bool = True

    # Node Management
    def add_base_image_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "input",
            "data": {
                "label": "Base Image",
                "image_url": "",
                "filters": [],
                "brightness": 100,
                "contrast": 100,
                "saturation": 100,
                "uploaded_at": datetime.datetime.now().isoformat()
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#1e40af", "color": "white", "border": "2px solid #3b82f6", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_style_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "default",
            "data": {
                "label": "Style Node",
                "style": self.current_style,
                "intensity": 0.7,
                "color_palette": ["#3b82f6", "#8b5cf6"],
                "created_at": datetime.datetime.now().isoformat()
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#7c3aed", "color": "white", "border": "2px solid #a855f7", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_ai_processor_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "default",
            "data": {
                "label": "AI Generator",
                "model": self.selected_model,
                "prompt": "",
                "negative_prompt": "",
                "steps": self.model_settings["steps"],
                "guidance_scale": self.model_settings["guidance_scale"],
                "seed": self.model_settings["seed"],
                "created_at": datetime.datetime.now().isoformat()
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#dc2626", "color": "white", "border": "2px solid #ef4444", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_text_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "default",
            "data": {
                "label": "Text Overlay",
                "text": "Sample Text",
                "font_family": "Arial",
                "font_size": 24,
                "font_weight": "normal",
                "color": "#ffffff",
                "alignment": "center",
                "effects": []
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#f59e0b", "color": "white", "border": "2px solid #fbbf24", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_filter_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "default",
            "data": {
                "label": "Filter",
                "filter_type": "None",
                "intensity": 0.5,
                "parameters": {}
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#8b5cf6", "color": "white", "border": "2px solid #a78bfa", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    def add_ab_test_node(self):
        new_node_id = str(len(self.nodes) + 1)
        new_node = {
            "id": new_node_id,
            "type": "default",
            "data": {
                "label": "A/B Test",
                "variants": 2,
                "test_parameter": "style",
                "test_values": [],
                "results": []
            },
            "position": {"x": random.randint(50, 400), "y": random.randint(50, 300)},
            "style": {"background": "#f97316", "color": "white", "border": "2px solid #fb923c", "borderRadius": "12px"}
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        self._save_version()

    # Canvas Operations
    def clear_canvas(self):
        self.nodes = []
        self.edges = []
        self.selected_node = {}
        self.selected_nodes = []
        self.preview_image = ""
        self.text_overlays = []
        self._save_version()

    def duplicate_selected_nodes(self):
        if self.selected_nodes:
            new_nodes = []
            for node_id in self.selected_nodes:
                original_node = next((n for n in self.nodes if n["id"] == node_id), None)
                if original_node:
                    new_node_id = str(len(self.nodes) + len(new_nodes) + 1)
                    new_node = original_node.copy()
                    new_node["id"] = new_node_id
                    new_node["position"] = {
                        "x": original_node["position"]["x"] + 50,
                        "y": original_node["position"]["y"] + 50
                    }
                    new_nodes.append(new_node)
            
            self.nodes.extend(new_nodes)
            self.analytics["nodes_created"] += len(new_nodes)
            self._save_version()

    def delete_selected_nodes(self):
        if self.selected_nodes:
            self.nodes = [n for n in self.nodes if n["id"] not in self.selected_nodes]
            self.edges = [e for e in self.edges if e["source"] not in self.selected_nodes and e["target"] not in self.selected_nodes]
            self.selected_nodes = []
            self.selected_node = {}
            self._save_version()

    def group_selected_nodes(self):
        if len(self.selected_nodes) > 1:
            # Create a group node
            group_id = f"group_{len([n for n in self.nodes if n['type'] == 'group']) + 1}"
            group_bounds = self._calculate_group_bounds(self.selected_nodes)
            
            group_node = {
                "id": group_id,
                "type": "group",
                "data": {
                    "label": f"Group ({len(self.selected_nodes)} nodes)",
                    "children": self.selected_nodes.copy()
                },
                "position": group_bounds["position"],
                "style": {
                    "background": "rgba(75, 85, 99, 0.1)",
                    "border": "2px dashed #6b7280",
                    "borderRadius": "8px",
                    "width": f"{group_bounds['width']}px",
                    "height": f"{group_bounds['height']}px"
                }
            }
            
            self.nodes.append(group_node)
            self.selected_nodes = [group_id]
            self._save_version()

    def _calculate_group_bounds(self, node_ids: List[str]) -> Dict[str, Any]:
        selected_positions = [n["position"] for n in self.nodes if n["id"] in node_ids]
        if not selected_positions:
            return {"position": {"x": 0, "y": 0}, "width": 200, "height": 100}
        
        min_x = min(pos["x"] for pos in selected_positions)
        min_y = min(pos["y"] for pos in selected_positions)
        max_x = max(pos["x"] for pos in selected_positions) + 200  # Assume node width
        max_y = max(pos["y"] for pos in selected_positions) + 100  # Assume node height
        
        return {
            "position": {"x": min_x - 20, "y": min_y - 20},
            "width": max_x - min_x + 40,
            "height": max_y - min_y + 40
        }

    # Connection Management
    def on_connect(self, connection):
        new_edge = {
            "id": f"e{connection['source']}-{connection['target']}",
            "source": connection["source"],
            "target": connection["target"],
            "animated": True,
            "style": {"stroke": self.accent_color, "strokeWidth": 2},
            "label": self._get_edge_label(connection["source"], connection["target"])
        }
        # Remove existing edge if it exists
        self.edges = [e for e in self.edges if e["id"] != new_edge["id"]]
        self.edges.append(new_edge)
        self._save_version()

    def _get_edge_label(self, source_id: str, target_id: str) -> str:
        source_node = next((n for n in self.nodes if n["id"] == source_id), None)
        target_node = next((n for n in self.nodes if n["id"] == target_id), None)
        
        if source_node and target_node:
            source_type = source_node.get("type", "default")
            target_type = target_node.get("type", "default")
            
            if source_type == "input" and target_type == "default":
                return "Process"
            elif "style" in source_node["data"].get("label", "").lower():
                return "Style"
            elif "filter" in source_node["data"].get("label", "").lower():
                return "Filter"
            
        return "Connect"

    def on_nodes_change(self, changes):
        # Handle node position changes and other updates
        for change in changes:
            if change.get("type") == "position" and "position" in change:
                for i, node in enumerate(self.nodes):
                    if node["id"] == change["id"]:
                        self.nodes[i]["position"] = change["position"]
            elif change.get("type") == "select":
                if change.get("selected"):
                    if change["id"] not in self.selected_nodes:
                        self.selected_nodes.append(change["id"])
                else:
                    if change["id"] in self.selected_nodes:
                        self.selected_nodes.remove(change["id"])

    def select_node(self, node_id: str):
        node = next((n for n in self.nodes if n["id"] == node_id), None)
        if node:
            self.selected_node = node
            if node_id not in self.selected_nodes:
                self.selected_nodes = [node_id]

    def deselect_node(self):
        self.selected_node = {}
        self.selected_nodes = []

    # AI Generation
    def generate_visual(self):
        # Simulate AI generation process
        self.preview_image = f"/api/placeholder/512/512"
        
        # Add to generation history
        generation_record = {
            "id": len(self.generation_history) + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "model": self.selected_model,
            "prompt": "Generated from canvas workflow",
            "image_url": self.preview_image,
            "settings": self.model_settings.copy(),
            "nodes_used": len(self.nodes)
        }
        self.generation_history.append(generation_record)
        self.analytics["images_generated"] += 1
        self._save_version()

    def run_ab_test(self):
        if not self.selected_node or "ab_test" not in self.selected_node["data"]["label"].lower():
            return
        
        variants = self.selected_node["data"].get("variants", 2)
        test_parameter = self.selected_node["data"].get("test_parameter", "style")
        
        # Generate test results
        results = []
        for i in range(variants):
            result = {
                "variant": f"Variant {chr(65 + i)}",  # A, B, C, etc.
                "image_url": f"/api/placeholder/400/400",
                "parameter_value": f"{test_parameter}_{i+1}",
                "score": random.randint(60, 95),
                "engagement": random.randint(100, 1000),
                "conversion": round(random.uniform(2.5, 8.5), 2)
            }
            results.append(result)
        
        self.ab_test_results = results
        self.current_ab_test = {
            "node_id": self.selected_node["id"],
            "parameter": test_parameter,
            "results": results,
            "created_at": datetime.datetime.now().isoformat()
        }
        self.analytics["ab_tests_run"] += 1

    # Template Management
    def load_template(self, template_id: str):
        template = next((t for t in self.templates if t["id"] == template_id), None)
        if not template:
            return
        
        # Template-specific node configurations
        template_configs = {
            "social_media": {
                "nodes": [
                    {"type": "input", "label": "Profile Image", "position": {"x": 100, "y": 100}},
                    {"type": "default", "label": "Brand Style", "position": {"x": 300, "y": 100}},
                    {"type": "default", "label": "Text Overlay", "position": {"x": 500, "y": 100}},
                    {"type": "output", "label": "Social Post", "position": {"x": 700, "y": 100}},
                ]
            },
            "banner_ad": {
                "nodes": [
                    {"type": "input", "label": "Product Image", "position": {"x": 100, "y": 150}},
                    {"type": "default", "label": "CTA Button", "position": {"x": 300, "y": 100}},
                    {"type": "default", "label": "Brand Logo", "position": {"x": 300, "y": 200}},
                    {"type": "output", "label": "Banner Ad", "position": {"x": 500, "y": 150}},
                ]
            },
            "logo_design": {
                "nodes": [
                    {"type": "default", "label": "Brand Name", "position": {"x": 100, "y": 100}},
                    {"type": "default", "label": "Icon/Symbol", "position": {"x": 100, "y": 200}},
                    {"type": "default", "label": "Color Palette", "position": {"x": 300, "y": 150}},
                    {"type": "output", "label": "Logo", "position": {"x": 500, "y": 150}},
                ]
            }
        }
        
        config = template_configs.get(template_id, template_configs["social_media"])
        self.nodes = []
        self.edges = []
        
        # Create nodes from template
        for i, node_config in enumerate(config["nodes"]):
            node_id = str(i + 1)
            node = {
                "id": node_id,
                "type": node_config["type"],
                "data": {"label": node_config["label"]},
                "position": node_config["position"],
                "style": self._get_node_style(node_config["type"])
            }
            self.nodes.append(node)
        
        # Create connections
        for i in range(len(self.nodes) - 1):
            edge = {
                "id": f"e{i+1}-{i+2}",
                "source": str(i + 1),
                "target": str(i + 2),
                "animated": True,
                "style": {"stroke": self.accent_color, "strokeWidth": 2}
            }
            self.edges.append(edge)
        
        self.selected_template = template_id
        self._save_version()

    def _get_node_style(self, node_type: str) -> Dict[str, str]:
        styles = {
            "input": {"background": "#1e40af", "color": "white", "border": "2px solid #3b82f6", "borderRadius": "12px"},
            "default": {"background": "#7c3aed", "color": "white", "border": "2px solid #a855f7", "borderRadius": "12px"},
            "output": {"background": "#059669", "color": "white", "border": "2px solid #10b981", "borderRadius": "12px"},
        }
        return styles.get(node_type, styles["default"])

    # Project Management
    def save_project(self, project_name: str):
        project = {
            "id": len(self.saved_projects) + 1,
            "name": project_name,
            "nodes": self.nodes.copy(),
            "edges": self.edges.copy(),
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "version": self.current_version,
            "preview_image": self.preview_image,
            "analytics": self.analytics.copy()
        }
        self.saved_projects.append(project)
        self.show_save_dialog = False

    def load_project(self, project_id: int):
        project = next((p for p in self.saved_projects if p["id"] == project_id), None)
        if project:
            self.nodes = project["nodes"].copy()
            self.edges = project["edges"].copy()
            self.preview_image = project.get("preview_image", "")
            self.current_version = project.get("version", 1)
            self.show_load_dialog = False
            self._save_version()

    # Version Control
    def _save_version(self):
        if self.auto_save_enabled:
            version = {
                "version": len(self.version_history) + 1,
                "timestamp": datetime.datetime.now().isoformat(),
                "nodes": self.nodes.copy(),
                "edges": self.edges.copy(),
                "description": f"Auto-save with {len(self.nodes)} nodes"
            }
            self.version_history.append(version)
            self.current_version = version["version"]
            
            # Keep only last 50 versions
            if len(self.version_history) > 50:
                self.version_history = self.version_history[-50:]

    def restore_version(self, version_number: int):
        version = next((v for v in self.version_history if v["version"] == version_number), None)
        if version:
            self.nodes = version["nodes"].copy()
            self.edges = version["edges"].copy()
            self.current_version = version["version"]

    # Export Functions
    def export_canvas(self):
        export_data = {
            "format": self.selected_export_format,
            "size": self.selected_export_size,
            "nodes": self.nodes,
            "edges": self.edges,
            "settings": {
                "width": self.custom_width if self.selected_export_size == "Custom" else None,
                "height": self.custom_height if self.selected_export_size == "Custom" else None,
                "quality": self.render_quality
            },
            "exported_at": datetime.datetime.now().isoformat()
        }
        
        self.analytics["exports_made"] += 1
        self.show_export_modal = False
        # In a real app, this would trigger the actual export process

    # Settings & Preferences
    def update_model_settings(self, setting: str, value: Any):
        self.model_settings[setting] = value

    def toggle_auto_save(self):
        self.auto_save_enabled = not self.auto_save_enabled

    def toggle_grid(self):
        self.grid_enabled = not self.grid_enabled

    def toggle_snap_to_grid(self):
        self.snap_to_grid = not self.snap_to_grid

    def toggle_rulers(self):
        self.rulers_enabled = not self.rulers_enabled

    def set_zoom_level(self, zoom: float):
        self.zoom_level = max(0.1, min(5.0, zoom))

    def set_render_quality(self, quality: str):
        self.render_quality = quality

    def toggle_real_time_preview(self):
        self.real_time_preview = not self.real_time_preview

    # Theme Management
    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.theme_background = "#f9fafb" if self.theme == "light" else "#1f2937"

    def set_accent_color(self, color: str):
        self.accent_color = color

    def create_custom_theme(self, theme_name: str, colors: Dict[str, str]):
        self.custom_themes[theme_name] = colors

    # Tutorial System
    def start_tutorial(self, tutorial_type: str = "basic"):
        self.tutorial_active = True
        self.tutorial_type = tutorial_type
        self.tutorial_step = 0
        self.show_tutorial = True

    def next_tutorial_step(self):
        max_steps = {"basic": 10, "advanced": 15, "expert": 20}
        if self.tutorial_step < max_steps.get(self.tutorial_type, 10) - 1:
            self.tutorial_step += 1
        else:
            self.end_tutorial()

    def prev_tutorial_step(self):
        if self.tutorial_step > 0:
            self.tutorial_step -= 1

    def end_tutorial(self):
        self.tutorial_active = False
        self.show_tutorial = False
        self.tutorial_step = 0

    # Collaboration Features
    def invite_collaborator(self, email: str, role: str = "editor"):
        new_collaborator = {
            "id": f"user_{len(self.collaborators) + 2}",
            "email": email,
            "role": role,  # owner, editor, viewer
            "status": "pending",
            "invited_at": datetime.datetime.now().isoformat(),
            "avatar": "/api/placeholder/40/40",
            "permissions": {
                "can_edit": role in ["owner", "editor"],
                "can_export": role == "owner",
                "can_invite": role == "owner"
            }
        }
        self.collaborators.append(new_collaborator)

    def update_collaborator_role(self, collaborator_id: str, new_role: str):
        for i, collab in enumerate(self.collaborators):
            if collab["id"] == collaborator_id:
                self.collaborators[i]["role"] = new_role
                self.collaborators[i]["permissions"] = {
                    "can_edit": new_role in ["owner", "editor"],
                    "can_export": new_role == "owner",
                    "can_invite": new_role == "owner"
                }
                break

    def remove_collaborator(self, collaborator_id: str):
        self.collaborators = [c for c in self.collaborators if c["id"] != collaborator_id]

    # Advanced AI Features
    def generate_prompt_suggestions(self, context: str = ""):
        suggestions = [
            "A modern minimalist design with clean lines and geometric shapes",
            "Vibrant cyberpunk aesthetic with neon colors and futuristic elements",
            "Elegant vintage style with ornate details and classic typography",
            "Bold abstract composition with dynamic shapes and gradients",
            "Professional corporate design with sophisticated color palette",
            "Playful illustration with hand-drawn elements and bright colors",
            "Luxury brand aesthetic with premium materials and gold accents",
            "Retro 80s design with synthwave colors and geometric patterns"
        ]
        return random.sample(suggestions, min(4, len(suggestions)))

    def auto_optimize_workflow(self):
        # Analyze current workflow and suggest optimizations
        optimizations = []
        
        # Check for unconnected nodes
        connected_nodes = set()
        for edge in self.edges:
            connected_nodes.add(edge["source"])
            connected_nodes.add(edge["target"])
        
        unconnected = [n for n in self.nodes if n["id"] not in connected_nodes]
        if unconnected:
            optimizations.append({
                "type": "unconnected_nodes",
                "message": f"{len(unconnected)} nodes are not connected to the workflow",
                "action": "Connect or remove unused nodes"
            })
        
        # Check for missing essential nodes
        node_types = [n.get("type", "default") for n in self.nodes]
        if "input" not in node_types:
            optimizations.append({
                "type": "missing_input",
                "message": "No input node found",
                "action": "Add a base image or input node"
            })
        
        if "output" not in node_types:
            optimizations.append({
                "type": "missing_output",
                "message": "No output node found",
                "action": "Add an output node to complete the workflow"
            })
        
        return optimizations

    # Performance Analytics
    def get_performance_metrics(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "workflow_complexity": self._calculate_complexity(),
            "generation_time_avg": random.uniform(2.5, 8.0),  # Mock data
            "success_rate": random.uniform(85, 98),  # Mock data
            "optimization_score": self._calculate_optimization_score()
        }

    def _calculate_complexity(self) -> str:
        node_count = len(self.nodes)
        edge_count = len(self.edges)
        
        if node_count <= 3 and edge_count <= 2:
            return "Simple"
        elif node_count <= 7 and edge_count <= 6:
            return "Moderate"
        elif node_count <= 12 and edge_count <= 15:
            return "Complex"
        else:
            return "Very Complex"

    def _calculate_optimization_score(self) -> int:
        score = 100
        
        # Deduct points for issues
        if len(self.nodes) > 15:
            score -= 10  # Too many nodes
        
        unconnected = len([n for n in self.nodes if n["id"] not in 
                          set(e["source"] for e in self.edges) | set(e["target"] for e in self.edges)])
        score -= unconnected * 5  # Unconnected nodes
        
        # Add points for good practices
        if any("ab_test" in n["data"].get("label", "").lower() for n in self.nodes):
            score += 10  # Has A/B testing
        
        if len(self.version_history) > 5:
            score += 5  # Good version control usage
        
        return max(0, min(100, score))
