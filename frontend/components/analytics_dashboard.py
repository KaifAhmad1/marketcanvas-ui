import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def analytics_dashboard():
    return rx.box(
        rx.vstack(
            rx.text("Analytics Dashboard", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.text(f"Nodes Created: {CanvasState.analytics['nodes_created']}", class_name="text-gray-400"),
            rx.text(f"Images Generated: {CanvasState.analytics['images_generated']}", class_name="text-gray-400"),
            rx.text(f"A/B Tests Run: {CanvasState.analytics['ab_tests_run']}", class_name="text-gray-400"),
            primary_button("Refresh Analytics", CanvasState.refresh_analytics, icon="refresh"),
            spacing="2",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 top-60",
        role="region",
        aria_label="Analytics dashboard",
    )
