import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def template_selector():
    return rx.box(
        rx.vstack(
            rx.text("Select Template", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.select(
                ["Social Media Post", "Ad Banner", "Branding Kit"],
                value=CanvasState.selected_template,
                on_change=CanvasState.set_selected_template,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Template selector",
            ),
            primary_button("Load Template", CanvasState.load_template, icon="template"),
            spacing="2",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 top-40",
        role="region",
        aria_label="Template selector",
    )
