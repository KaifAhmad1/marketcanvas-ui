import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def theme_builder():
    return rx.box(
        rx.vstack(
            rx.text("Theme Builder", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.select(
                ["Dark", "Light", "Custom"],
                value=CanvasState.theme,
                on_change=CanvasState.set_theme,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Theme selector",
            ),
            rx.color_picker(
                value=CanvasState.theme_background,
                on_change=CanvasState.set_theme_background,
                class_name="w-full",
                aria_label="Background color picker",
            ),
            rx.text("Background Color", font_size="0.9em", class_name="text-gray-400"),
            rx.select(
                ["Inter", "Roboto", "Poppins"],
                value=CanvasState.theme_font,
                on_change=CanvasState.set_theme_font,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Font selector",
            ),
            rx.text("Font Family", font_size="0.9em", class_name="text-gray-400"),
            primary_button("Apply Theme", CanvasState.apply_theme, icon="check"),
            spacing="2",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 top-20",
        role="region",
        aria_label="Theme builder",
    )
