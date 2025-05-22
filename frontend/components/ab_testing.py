import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def ab_testing_panel():
    return rx.cond(
        CanvasState.ab_test_results,
        rx.box(
            rx.vstack(
                rx.text("A/B Test Results", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
                rx.foreach(
                    CanvasState.ab_test_results,
                    lambda result, index: rx.box(
                        rx.image(src=result["image"], width="100%", border_radius="8px", class_name="shadow-md"),
                        rx.text(f"Variant {index + 1}: {result['parameter']}", class_name="text-gray-400"),
                        rx.text(f"Score: {result['score']}%", class_name="text-gray-400"),
                        spacing="2",
                    ),
                ),
                primary_button("Regenerate Variants", CanvasState.run_ab_test, icon="refresh"),
                spacing="4",
                padding="1rem",
                class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
            ),
            class_name="absolute right-4 bottom-4",
            role="region",
            aria_label="A/B testing results",
        ),
        rx.box(),
    )
