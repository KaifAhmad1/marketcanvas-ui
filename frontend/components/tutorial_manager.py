import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button, modal

def tutorial_manager():
    return modal(
        title="Interactive Tutorial",
        content=rx.vstack(
            rx.text(
                rx.cond(
                    CanvasState.tutorial_step < len(CanvasState.tutorial_steps),
                    CanvasState.tutorial_steps[CanvasState.tutorial_step]["description"],
                    "Tutorial Complete!",
                ),
                class_name="text-gray-200",
            ),
            rx.progress(
                value=(CanvasState.tutorial_step + 1) / len(CanvasState.tutorial_steps) * 100,
                class_name="w-full",
            ),
            rx.hstack(
                primary_button("Previous", CanvasState.prev_tutorial_step, icon="arrow-left"),
                primary_button("Next", CanvasState.next_tutorial_step, icon="arrow-right"),
                spacing="2",
            ),
            spacing="4",
        ),
        is_open=CanvasState.show_tutorial,
        on_close=CanvasState.end_tutorial,
        class_name="bg-gray-800 border border-gray-700 rounded-lg glass",
        role="dialog",
        aria_label="Tutorial modal",
    )
