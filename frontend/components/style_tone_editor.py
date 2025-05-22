import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def style_tone_editor():
    return rx.box(
        rx.vstack(
            rx.text("Global Style & Tone", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.select(
                ["Modern", "Vintage", "Minimalist", "Luxury", "Cyberpunk"],
                value=CanvasState.current_style,
                on_change=CanvasState.set_global_style,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Global style selector",
            ),
            rx.slider(
                value=CanvasState.current_style_intensity,
                min=0,
                max=1,
                step=0.1,
                on_change=CanvasState.set_global_style_intensity,
                class_name="w-full",
                aria_label="Global style intensity slider",
            ),
            rx.text("Style Intensity", font_size="0.9em", class_name="text-gray-400"),
            rx.select(
                ["Professional", "Playful", "Elegant", "Bold", "Futuristic"],
                value=CanvasState.current_tone,
                on_change=CanvasState.set_global_tone,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Global tone selector",
            ),
            rx.slider(
                value=CanvasState.current_tone_intensity,
                min=0,
                max=1,
                step=0.1,
                on_change=CanvasState.set_global_tone_intensity,
                class_name="w-full",
                aria_label="Global tone intensity slider",
            ),
            rx.text("Tone Intensity", font_size="0.9em", class_name="text-gray-400"),
            rx.color_picker(
                value=CanvasState.accent_color,
                on_change=CanvasState.set_accent_color,
                class_name="w-full",
                aria_label="Accent color picker",
            ),
            primary_button("Apply to Canvas", CanvasState.apply_global_styles, icon="check"),
            spacing="4",
            padding="1rem",
            class_name="w-80 bg-gray-		space-y-4 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 bottom-4",
        role="region",
        aria_label="Style and tone editor",
    )
