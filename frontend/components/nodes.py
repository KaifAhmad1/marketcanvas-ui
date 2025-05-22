import reflex as rx
from typing import Any, Dict, List

class CustomNode(rx.Component):
    library = "reactflow@11.10.1"
    tag = "CustomNode"
    
    data: rx.Var[Dict[str, Any]]
    id: rx.Var[str]
    type: rx.Var[str]
    position: rx.Var[Dict[str, float]]
    width: rx.Var[int]
    height: rx.Var[int]

def create_custom_node(node_type: str, node_id: str, label: str, position: Dict[str, float], data: Dict[str, Any] = {}):
    node_styles = {
        "base_image": "bg-blue-900 border-blue-500 text-blue-200",
        "secondary_image": "bg-green-900 border-green-500 text-green-200",
        "style": "bg-purple-900 border-purple-500 text-purple-200",
        "processor": "bg-pink-900 border-pink-500 text-pink-200",
        "ab_test": "bg-orange-900 border-orange-500 text-orange-200",
        "template": "bg-teal-900 border-teal-500 text-teal-200",
        "output": "bg-yellow-900 border-yellow-500 text-yellow-200",
    }
    icon = data.get("icon", node_type)
    return CustomNode.create(
        id=node_id,
        type=node_type,
        data={"label": label, "icon": icon, **data},
        position=position,
        width=data.get("width", 200),
        height=data.get("height", 100),
        class_name=f"border-2 rounded-lg p-4 shadow-md {node_styles.get(node_type, 'bg-gray-900 border-gray-500 text-gray-200')} transition-all hover:scale-105",
        aria_label=f"{node_type.replace('_', ' ')} node",
    )

def base_image_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("base_image", node_id, "Base Image", position, {"image": "", "edit": "none", "icon": "image"})

def secondary_image_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("secondary_image", node_id, "Secondary Image", position, {"image": "", "icon": "plus-circle"})

def style_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("style", node_id, "Style", position, {"style": "modern", "tone": "professional", "style_intensity": 0.5, "icon": "palette"})

def ai_processor_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("processor", node_id, "AI Processor", position, {"llm": "DALL-E 3", "prompt": "", "guidance_scale": 7.5, "icon": "cpu"})

def ab_test_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("ab_test", node_id, "A/B Test", position, {"variants": 2, "parameter": "style", "icon": "split"})

def template_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("template", node_id, "Template", position, {"template_type": "social_media", "icon": "template"})

def output_node(node_id: str, position: Dict[str, float]):
    return create_custom_node("output", node_id, "Output", position, {"icon": "output"})
