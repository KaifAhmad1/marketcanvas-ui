import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def preview_panel():
    return rx.box(
        rx.vstack(
            rx.text("WYSIWYG Preview", font_weight="bold", font_size="1.5em", class_name="text-gray-200"),
            rx.cond(
                CanvasState.preview_image,
                rx.box(
                    rx.image(src=CanvasState.preview_image, width="100%", border_radius="8px", class_name="shadow-md"),
                    rx.cond(
                        CanvasState.text_overlay,
                        rx.text(
                            CanvasState.text_overlay,
                            style={
                                "position": "absolute",
                                "left": f"{CanvasState.text_position['x']}px",
                                "top": f"{CanvasState.text_position['y']}px",
                                "color": CanvasState.text_style["color"],
                                "fontSize": f"{CanvasState.text_style['fontSize']}px",
                                "fontWeight": CanvasState.text_style["fontWeight"],
                            },
                            class_name="motion-reduce:animate-pulse",
                        ),
                        rx.box(),
                    ),
                    rx.input(
                        placeholder="Add text overlay",
                        on_change=CanvasState.add_text_overlay,
                        class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200 mt-2",
                        aria_label="Text overlay input",
                    ),
                    rx.hstack(
                        rx.select(
                            ["16px", "24px", "32px"],
                            value=f"{CanvasState.text_style['fontSize']}px",
                            on_change=CanvasState.update_text_font_size,
                            class_name="p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Text font size selector",
                        ),
                        rx.select(
                            ["normal", "bold"],
                            value=CanvasState.text_style["fontWeight"],
                            on_change=CanvasState.update_text_font_weight,
                            class_name="p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                            aria_label="Text font weight selector",
                        ),
                        rx.color_picker(
                            value=CanvasState.text_style["color"],
                            on_change=CanvasState.update_text_color,
                            class_name="w-12",
                            aria_label="Text color picker",
                        ),
                        spacing="2",
                    ),
                    primary_button("Upload Logo", CanvasState.upload_logo, icon="upload"),
                    primary_button(
                        rx.cond(CanvasState.text_dragging, "Lock Position", "Drag Text"),
                        CanvasState.enable_text_drag,
                        icon="move",
                    ),
                    class_name="relative",
                ),
                rx.text("No preview available", class_name="text-gray-400"),
            ),
            rx.text(
                f"Style: {CanvasState.current_style} | Tone: {CanvasState.current_tone} | LLM: {CanvasState.default_llm}",
                font_size="0.9em",
                class_name="text-gray-400",
            ),
            primary_button("Generate Visual", CanvasState.generate_visual, icon="sparkles"),
            spacing="4",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="w-80",
        role="region",
        aria_label="Preview panel",
    )
