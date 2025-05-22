import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def llm_selector():
    return rx.box(
        rx.vstack(
            rx.text("Image Generation LLM", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.select(
                ["DALL-E 3", "Stable Diffusion 3", "Flux.1"],
                value=CanvasState.default_llm,
                on_change=CanvasState.set_default_llm,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="LLM selector",
            ),
            rx.slider(
                value=CanvasState.default_guidance_scale,
                min=1,
                max=20,
                step=0.5,
                on_change=CanvasState.set_default_guidance_scale,
                class_name="w-full",
                aria_label="Guidance scale slider",
            ),
            rx.text("Guidance Scale", font_size="0.9em", class_name="text-gray-400"),
            rx.number_input(
                value=CanvasState.default_sampling_steps,
                min=10,
                max=100,
                on_change=CanvasState.set_default_sampling_steps,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
                aria_label="Sampling steps input",
            ),
            rx.text("Sampling Steps", font_size="0.9em", class_name="text-gray-400"),
            primary_button("Apply to Processors", CanvasState.apply_default_llm, icon="check"),
            spacing="2",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 top-4",
        role="region",
        aria_label="LLM selector",
    )
