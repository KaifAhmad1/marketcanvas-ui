import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def property_panel():
    return rx.cond(
        CanvasState.selected_node,
        rx.box(
            rx.vstack(
                rx.text(f"Editing Node: {CanvasState.selected_node['id']}", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
                rx.input(
                    placeholder="Node Label",
                    value=CanvasState.selected_node.get("data", {}).get("label", ""),
                    on_change=CanvasState.update_node_label,
                    class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                    aria_label="Node label input",
                ),
                rx.select(
                    ["Base Image", "Secondary Image", "Style", "AI Processor", "A/B Test", "Template", "Output"],
                    value=CanvasState.selected_node.get("type", "").replace("_", " ").title(),
                    on_change=CanvasState.update_node_type,
                    class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                    aria_label="Node type selector",
                ),
                rx.cond(
                    CanvasState.selected_node.get("type") == "style",
                    rx.vstack(
                        rx.select(
                            ["Modern", "Vintage", "Minimalist", "Luxury", "Cyberpunk"],
                            value=CanvasState.selected_node.get("data", {}).get("style", "Modern"),
                            on_change=CanvasState.update_node_style,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Style selector",
                        ),
                        rx.select(
                            ["Professional", "Playful", "Elegant", "Bold", "Futuristic"],
                            value=CanvasState.selected_node.get("data", {}).get("tone", "Professional"),
                            on_change=CanvasState.update_node_tone,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Tone selector",
                        ),
                        rx.slider(
                            value=CanvasState.selected_node.get("data", {}).get("style_intensity", 0.5),
                            min=0,
                            max=1,
                            step=0.1,
                            on_change=CanvasState.update_style_intensity,
                            class_name="w-full",
                            aria_label="Style intensity slider",
                        ),
                        rx.text("Style Intensity", font_size="0.9em", class_name="text-gray-400"),
                        spacing="2",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    CanvasState.selected_node.get("type") == "processor",
                    rx.vstack(
                        rx.select(
                            ["DALL-E 3", "Stable Diffusion 3", "Flux.1"],
                            value=CanvasState.selected_node.get("data", {}).get("llm", "DALL-E 3"),
                            on_change=CanvasState.update_node_llm,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="LLM selector",
                        ),
                        rx.text_area(
                            placeholder="Enter custom prompt (e.g., 'A futuristic watch on a neon cityscape')",
                            value=CanvasState.selected_node.get("data", {}).get("prompt", ""),
                            on_change=CanvasState.update_node_prompt,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200 h-24",
                            aria_label="Custom prompt input",
                        ),
                        primary_button("Suggest Prompt", CanvasState.suggest_prompt, icon="light-bulb"),
                        rx.slider(
                            value=CanvasState.selected_node.get("data", {}).get("guidance_scale", 7.5),
                            min=1,
                            max=20,
                            step=0.5,
                            on_change=CanvasState.update_guidance_scale,
                            class_name="w-full",
                            aria_label="Guidance scale slider",
                        ),
                        rx.text("Guidance Scale", font_size="0.9em", class_name="text-gray-400"),
                        spacing="2",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    CanvasState.selected_node.get("type") == "ab_test",
                    rx.vstack(
                        rx.select(
                            ["Style", "Tone", "Prompt"],
                            value=CanvasState.selected_node.get("data", {}).get("parameter", "Style"),
                            on_change=CanvasState.update_ab_test_parameter,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="A/B test parameter selector",
                        ),
                        rx.number_input(
                            value=CanvasState.selected_node.get("data", {}).get("variants", 2),
                            min=2,
                            max=5,
                            on_change=CanvasState.update_ab_test_variants,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Number of variants input",
                        ),
                        rx.text("Number of Variants", font_size="0.9em", class_name="text-gray-400"),
                        spacing="2",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    CanvasState.selected_node.get("type") == "template",
                    rx.vstack(
                        rx.select(
                            ["Social Media Post", "Ad Banner", "Branding Kit"],
                            value=CanvasState.selected_node.get("data", {}).get("template_type", "Social Media Post"),
                            on_change=CanvasState.update_template_type,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Template type selector",
                        ),
                        spacing="2",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    CanvasState.selected_node.get("type").in_(["base_image", "secondary_image"]),
                    primary_button("Upload Image", CanvasState.upload_image, icon="upload"),
                    rx.box(),
                ),
                rx.cond(
                    CanvasState.selected_node.get("type") == "base_image",
                    rx.vstack(
                        rx.select(
                            ["Crop", "Rotate", "Adjust Brightness", "Apply Filter"],
                            placeholder="Select Edit",
                            on_change=CanvasState.apply_image_edit,
                            class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Image edit selector",
                        ),
                        spacing="2",
                    ),
                    rx.box(),
                ),
                rx.vstack(
                    rx.select(
                        ["image", "plus-circle", "palette", "cpu", "split", "template", "output"],
                        value=CanvasState.selected_node.get("data", {}).get("icon", "image"),
                        on_change=CanvasState.update_node_icon,
                        class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                        aria_label="Node icon selector",
                    ),
                    rx.number_input(
                        value=CanvasState.selected_node.get("width", 200),
                        min=100,
                        max=400,
                        on_change=CanvasState.update_node_width,
                        class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                        aria_label="Node width input",
                    ),
                    rx.number_input(
                        value=CanvasState.selected_node.get("height", 100),
                        min=50,
                        max=200,
                        on_change=CanvasState.update_node_height,
                        class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                        aria_label="Node height input",
                    ),
                    rx.text("Node Customization", font_size="0.9em", class_name="text-gray-400"),
                    spacing="2",
                ),
                spacing="4",
                padding="1rem",
                class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
            ),
            class_name="absolute right-4 top-4",
            role="dialog",
            aria_label="Node properties panel",
        ),
        rx.box(),
    )
