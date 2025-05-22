import reflex as rx
from typing import Any, Dict, List
import random
import json
from .ui_components import toast

initial_nodes = [
    {"id": "1", "type": "base_image", "data": {"label": "Base Image", "image": "", "edit": "none", "icon": "image", "width": 200, "height": 100}, "position": {"x": 100, "y": 50}},
    {"id": "2", "type": "secondary_image", "data": {"label": "Secondary Image", "image": "", "icon": "plus-circle", "width": 200, "height": 100}, "position": {"x": 100, "y": 200}},
    {"id": "3", "type": "style", "data": {"label": "Style", "style": "Modern", "tone": "Professional", "style_intensity": 0.5, "icon": "palette", "width": 200, "height": 100}, "position": {"x": 300, "y": 125}},
    {"id": "4", "type": "processor", "data": {"label": "AI Processor", "llm": "DALL-E 3", "prompt": "", "guidance_scale": 7.5, "icon": "cpu", "width": 200, "height": 100}, "position": {"x": 500, "y": 150}},
    {"id": "5", "type": "ab_test", "data": {"label": "A/B Test", "variants": 2, "parameter": "style", "icon": "split", "width": 200, "height": 100}, "position": {"x": 700, "y": 100}},
    {"id": "6", "type": "template", "data": {"label": "Template", "template_type": "social_media", "icon": "template", "width": 200, "height": 100}, "position": {"x": 900, "y": 50}},
    {"id": "7", "type": "output", "data": {"label": "Output", "icon": "output", "width": 200, "height": 100}, "position": {"x": 900, "y": 150}},
]

initial_edges = [
    {"id": "e1-3", "source": "1", "target": "3", "label": "Style", "animated": True, "type": "style"},
    {"id": "e2-3", "source": "2", "target": "3", "label": "Style", "animated": True, "type": "style"},
    {"id": "e3-4", "source": "3", "target": "4", "label": "Process", "animated": True, "type": "image"},
    {"id": "e4-5", "source": "4", "target": "5", "label": "Test", "animated": True, "type": "test"},
    {"id": "e5-6", "source": "5", "target": "6", "label": "Template", "animated": True, "type": "image"},
    {"id": "e6-7", "source": "6", "target": "7", "label": "Output", "animated": True, "type": "image"},
]

tutorial_steps = [
    {"description": "Add a base image node to start your workflow."},
    {"description": "Upload an image to the base image node."},
    {"description": "Add a style node and select a style like 'Modern'."},
    {"description": "Connect the base image to the style node."},
    {"description": "Add an AI processor node and set a custom prompt."},
    {"description": "Connect the style node to the AI processor."},
    {"description": "Add a template node for a predefined layout."},
    {"description": "Connect the AI processor to the template node."},
    {"description": "Add an output node and connect the template to it."},
    {"description": "Click 'Generate Visual' to see the result in the preview."},
]

class CanvasState(rx.State):
    nodes: List[Dict[str, Any]] = initial_nodes
    edges: List[Dict[str, Any]] = initial_edges
    selected_node: Dict[str, Any] = {}
    preview_image: str = ""
    current_style: str = "Modern"
    current_tone: str = "Professional"
    current_style_intensity: float = 0.5
    current_tone_intensity: float = 0.5
    default_llm: str = "DALL-E 3"
    default_guidance_scale: float = 7.5
    default_sampling_steps: int = 50
    theme: str = "dark"
    accent_color: str = "#3b82f6"
    theme_background: str = "#555"
    show_context_menu: bool = False
    context_node_id: str = ""
    show_tutorial: bool = False
    tutorial_step: int = 0
    tutorial_steps: List[Dict[str, str]] = tutorial_steps
    ab_test_results: List[Dict[str, Any]] = []
    text_overlay: str = ""
    text_position: Dict[str, float] = {"x": 0, "y": 0}
    text_style: Dict[str, Any] = {"color": "#ffffff", "fontSize": 24, "fontWeight": "normal"}
    text_dragging: bool = False
    collaborators: List[Dict[str, Any]] = [{"name": "Guest", "active": True}]
    selected_template: str = "Social Media Post"
    show_template_selector: bool = False
    analytics: Dict[str, int] = {"nodes_created": 0, "images_generated": 0, "ab_tests_run": 0}
    logo_image: str = ""

    def add_base_image_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "base_image",
            "data": {"label": "Base Image", "image": "", "edit": "none", "icon": "image", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("Base Image Node Added", "success")

    def add_secondary_image_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "secondary_image",
            "data": {"label": "Secondary Image", "image": "", "icon": "plus-circle", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("Secondary Image Node Added", "success")

    def add_style_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "style",
            "data": {"label": "Style", "style": self.current_style, "tone": self.current_tone, "style_intensity": self.current_style_intensity, "icon": "palette", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("Style Node Added", "success")

    def add_ai_processor_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "processor",
            "data": {"label": "AI Processor", "llm": self.default_llm, "prompt": "", "guidance_scale": self.default_guidance_scale, "sampling_steps": self.default_sampling_steps, "icon": "cpu", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("AI Processor Node Added", "success")

    def add_ab_test_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "ab_test",
            "data": {"label": "A/B Test", "variants": 2, "parameter": "style", "icon": "split", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("A/B Test Node Added", "success")

    def add_template_node(self):
        new_node_id = f"{len(self.nodes) + 1}"
        new_node = {
            "id": new_node_id,
            "type": "template",
            "data": {"label": "Template", "template_type": self.selected_template, "icon": "template", "width": 200, "height": 100},
            "position": {"x": random.randint(0, 500), "y": random.randint(0, 500)},
            "draggable": True,
        }
        self.nodes.append(new_node)
        self.analytics["nodes_created"] += 1
        toast("Template Node Added", "success")

    def clear_canvas(self):
        self.nodes = []
        self.edges = []
        self.selected_node = {}
        self.preview_image = ""
        self.ab_test_results = []
        toast("Canvas Cleared", "success")

    def on_connect(self, new_edge):
        for i, edge in enumerate(self.edges):
            if edge["id"] == f"e{new_edge['source']}-{new_edge['target']}":
                del self.edges[i]
                break
        edge_type = "image" if new_edge["source"] in [n["id"] for n in self.nodes if n["type"] in ["base_image", "secondary_image"]] else "style" if new_edge["target"] in [n["id"] for n in self.nodes if n["type"] == "style"] else "test"
        self.edges.append({
            "id": f"e{new_edge['source']}-{new_edge['target']}",
            "source": new_edge["source"],
            "target": new_edge["target"],
            "label": edge_type.capitalize(),
            "animated": True,
            "type": edge_type,
        })
        toast("Nodes Connected", "success")

    def on_nodes_change(self, node_changes: List[Dict[str, Any]]):
        map_id_to_new_position = {}
        for change in node_changes:
            if change["type"] == "position" and change.get("dragging"):
                map_id_to_new_position[change["id"]] = change["position"]
        for i, node in enumerate(self.nodes):
            if node["id"] in map_id_to_new_position:
                self.nodes[i]["position"] = map_id_to_new_position[node["id"]]

    def deselect_node(self):
        self.selected_node = {}
        self.show_context_menu = False

    def open_context_menu(self, event):
        self.context_node_id = event["id"]
        self.show_context_menu = True

    def close_context_menu(self):
        self.show_context_menu = False

    def duplicate_node(self):
        if self.context_node_id:
            for node in self.nodes:
                if node["id"] == self.context_node_id:
                    new_node_id = f"{len(self.nodes) + 1}"
                    new_node = node.copy()
                    new_node["id"] = new_node_id
                    new_node["position"] = {"x": node["position"]["x"] + 50, "y": node["position"]["y"] + 50}
                    self.nodes.append(new_node)
                    self.analytics["nodes_created"] += 1
                    toast("Node Duplicated", "success")
                    break
        self.show_context_menu = False

    def delete_node(self):
        if self.context_node_id:
            self.nodes = [node for node in self.nodes if node["id"] != self.context_node_id]
            self.edges = [edge for edge in self.edges if edge["source"] != self.context_node_id and edge["target"] != self.context_node_id]
            self.selected_node = {}
            toast("Node Deleted", "success")
        self.show_context_menu = False

    def group_nodes(self):
        # Placeholder for node grouping logic
        self.show_context_menu = False
        toast("Node Grouping Not Implemented", "warning")

    def customize_node(self):
        if self.context_node_id:
            for node in self.nodes:
                if node["id"] == self.context_node_id:
                    self.selected_node = node
                    break
        self.show_context_menu = False

    def resize_node(self, event):
        node_id = event["id"]
        for i, node in enumerate(self.nodes):
            if node["id"] == node_id:
                self.nodes[i]["width"] = event["width"]
                self.nodes[i]["height"] = event["height"]
                break

    def update_node_label(self, label: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["label"] = label
                    self.selected_node = self.nodes[i]
                    toast("Label Updated", "success")

    def update_node_type(self, node_type: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["type"] = node_type.lower().replace(" ", "_")
                    self.selected_node = self.nodes[i]
                    toast("Node Type Updated", "success")

    def update_node_style(self, style: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["style"] = style
                    self.selected_node = self.nodes[i]
                    self.current_style = style
                    toast("Style Updated", "success")

    def update_node_tone(self, tone: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["tone"] = tone
                    self.selected_node = self.nodes[i]
                    self.current_tone = tone
                    toast("Tone Updated", "success")

    def update_style_intensity(self, intensity: float):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["style_intensity"] = intensity
                    self.selected_node = self.nodes[i]
                    self.current_style_intensity = intensity
                    toast("Style Intensity Updated", "success")

    def update_node_llm(self, llm: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["llm"] = llm
                    self.selected_node = self.nodes[i]
                    self.default_llm = llm
                    toast("LLM Updated", "success")

    def update_guidance_scale(self, scale: float):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["guidance_scale"] = scale
                    self.selected_node = self.nodes[i]
                    self.default_guidance_scale = scale
                    toast("Guidance Scale Updated", "success")

    def update_sampling_steps(self, steps: int):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["sampling_steps"] = steps
                    self.selected_node = self.nodes[i]
                    self.default_sampling_steps = steps
                    toast("Sampling Steps Updated", "success")

    def update_ab_test_parameter(self, parameter: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["parameter"] = parameter
                    self.selected_node = self.nodes[i]
                    toast("A/B Test Parameter Updated", "success")

    def update_ab_test_variants(self, variants: int):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["variants"] = variants
                    self.selected_node = self.nodes[i]
                    toast("A/B Test Variants Updated", "success")

    def update_template_type(self, template_type: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["template_type"] = template_type
                    self.selected_node = self.nodes[i]
                    self.selected_template = template_type
                    toast("Template Type Updated", "success")

    def update_node_icon(self, icon: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["icon"] = icon
                    self.selected_node = self.nodes[i]
                    toast("Node Icon Updated", "success")

    def update_node_width(self, width: int):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["width"] = width
                    self.selected_node = self.nodes[i]
                    toast("Node Width Updated", "success")

    def update_node_height(self, height: int):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["height"] = height
                    self.selected_node = self.nodes[i]
                    toast("Node Height Updated", "success")

    def upload_image(self):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["image"] = "/static/sample_image.png"  # Replace with actual upload
                    self.selected_node = self.nodes[i]
                    toast("Image Uploaded", "success")
        else:
            toast("No Node Selected", "error")

    def upload_logo(self):
        self.logo_image = "/static/sample_logo.png"  # Replace with actual upload
        toast("Logo Uploaded", "success")

    def apply_image_edit(self, edit: str):
        if self.selected_node:
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["edit"] = edit
                    self.selected_node = self.nodes[i]
                    toast(f"Applied {edit}", "success")
        else:
            toast("No Node Selected", "error")

    def set_global_style(self, style: str):
        self.current_style = style
        toast("Global Style Updated", "success")

    def set_global_tone(self, tone: str):
        self.current_tone = tone
        toast("Global Tone Updated", "success")

    def set_global_style_intensity(self, intensity: float):
        self.current_style_intensity = intensity
        toast("Global Style Intensity Updated", "success")

    def set_global_tone_intensity(self, intensity: float):
        self.current_tone_intensity = intensity
        toast("Global Tone Intensity Updated", "success")

    def set_default_llm(self, llm: str):
        self.default_llm = llm
        toast("Default LLM Updated", "success")

    def set_default_guidance_scale(self, scale: float):
        self.default_guidance_scale = scale
        toast("Default Guidance Scale Updated", "success")

    def set_default_sampling_steps(self, steps: int):
        self.default_sampling_steps = steps
        toast("Default Sampling Steps Updated", "success")

    def set_accent_color(self, color: str):
        self.accent_color = color
        self.theme_background = "#555" if self.theme == "dark" else "#888"
        toast("Accent Color Updated", "success")

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.theme_background = "#555" if self.theme == "dark" else "#888"
        toast("Theme Toggled", "success")

    def apply_global_styles(self):
        for i, node in enumerate(self.nodes):
            if node["type"] == "style":
                self.nodes[i]["data"]["style"] = self.current_style
                self.nodes[i]["data"]["tone"] = self.current_tone
                self.nodes[i]["data"]["style_intensity"] = self.current_style_intensity
                self.nodes[i]["data"]["tone_intensity"] = self.current_tone_intensity
        toast("Global Styles Applied", "success")

    def apply_default_llm(self):
        for i, node in enumerate(self.nodes):
            if node["type"] == "processor":
                self.nodes[i]["data"]["llm"] = self.default_llm
                self.nodes[i]["data"]["guidance_scale"] = self.default_guidance_scale
                self.nodes[i]["data"]["sampling_steps"] = self.default_sampling_steps
        toast("Default LLM Applied", "success")

    def generate_visual(self):
        self.preview_image = "/static/sample_preview.png"  # Replace with backend call
        self.analytics["images_generated"] += 1
        toast("Visual Generated", "success")

    def run_ab_test(self):
        if self.selected_node and self.selected_node["type"] == "ab_test":
            variants = self.selected_node["data"]["variants"]
            parameter = self.selected_node["data"]["parameter"]
            self.ab_test_results = [
                {"image": f"/static/sample_variant_{i+1}.png", "parameter": f"{parameter} Variant {i+1}", "score": random.randint(70, 95)}
                for i in range(variants)
            ]  # Replace with backend call
            self.analytics["ab_tests_run"] += 1
            toast("A/B Test Run", "success")
        else:
            toast("No A/B Test Node Selected", "error")

    def add_text_overlay(self, text: str):
        self.text_overlay = text
        toast("Text Overlay Added", "success")

    def update_text_color(self, color: str):
        self.text_style["color"] = color
        toast("Text Color Updated", "success")

    def update_text_font_size(self, size: str):
        self.text_style["fontSize"] = int(size.replace("px", ""))
        toast("Text Font Size Updated", "success")

    def update_text_font_weight(self, weight: str):
        self.text_style["fontWeight"] = weight
        toast("Text Font Weight Updated", "success")

    def enable_text_drag(self):
        self.text_dragging = not self.text_dragging
        toast("Text Dragging Toggled", "success")

    def update_text_position(self, position: Dict[str, float]):
        self.text_position = position
        toast("Text Position Updated", "success")

    def start_tutorial(self):
        self.show_tutorial = True
        self.tutorial_step = 0
        toast("Tutorial Started", "success")

    def next_tutorial_step(self):
        if self.tutorial_step < len(self.tutorial_steps) - 1:
            self.tutorial_step += 1
        else:
            self.end_tutorial()
        toast("Next Tutorial Step", "success")

    def prev_tutorial_step(self):
        if self.tutorial_step > 0:
            self.tutorial_step -= 1
        toast("Previous Tutorial Step", "success")

    def end_tutorial(self):
        self.show_tutorial = False
        self.tutorial_step = 0
        toast("Tutorial Ended", "success")

    def invite_collaborator(self):
        # Placeholder for collaboration logic
        self.collaborators.append({"name": f"User {len(self.collaborators) + 1}", "active": True})
        toast("Collaborator Invited", "success")

    def set_selected_template(self, template: str):
        self.selected_template = template
        toast("Template Selected", "success")

    def show_template_selector(self):
        self.show_template_selector = True
        toast("Template Selector Opened", "success")

    def close_template_selector(self):
        self.show_template_selector = False
        toast("Template Selector Closed", "success")

    def load_template(self):
        # Placeholder for template loading logic
        self.nodes = initial_nodes  # Mock template load
        self.edges = initial_edges
        toast(f"{self.selected_template} Template Loaded", "success")
        self.show_template_selector = False

    def load_template_confirm(self):
        self.load_template()

    def export_canvas(self):
        canvas_data = {"nodes": self.nodes, "edges": self.edges}
        # Placeholder for export logic (e.g., JSON, PNG, PDF)
        toast("Canvas Exported as JSON", "success")

    def refresh_analytics(self):
        # Placeholder for analytics refresh
        toast("Analytics Refreshed", "success")

    def suggest_prompt(self):
        if self.selected_node and self.selected_node["type"] == "processor":
            # Mock Grok suggestion
            suggested_prompt = f"A {self.current_style.lower()} {self.current_tone.lower()} advertisement featuring a product"
            for i, node in enumerate(self.nodes):
                if node["id"] == self.selected_node["id"]:
                    self.nodes[i]["data"]["prompt"] = suggested_prompt
                    self.selected_node = self.nodes[i]
                    toast("Prompt Suggested", "success")
                    break
        else:
            toast("No AI Processor Node Selected", "error")
