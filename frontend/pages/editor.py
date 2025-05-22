# frontend/pages/editor.py
import reflex as rx
from ..components.enhanced_canvas import enhanced_toolbar, enhanced_canvas, properties_panel, layers_panel, ai_assistant_panel, live_preview_panel
from ..components.ui_components import modal, primary_button, card
from ..state.canvas_state import CanvasState

def _export_modal_content():
    return rx.vstack(
        rx.text("Format", size="2", weight="medium"),
        rx.select.root(
            rx.select.trigger(placeholder="Select format", width="100%"),
            rx.select.content(
                rx.foreach(CanvasState.export_formats, lambda fmt: rx.select.item(fmt, value=fmt))
            ),
            value=CanvasState.selected_export_format,
            on_change=lambda val: setattr(CanvasState, "selected_export_format", val),
            width="100%"
        ),
        rx.text("Size", size="2", weight="medium", margin_top="1rem"),
        rx.select.root(
            rx.select.trigger(placeholder="Select size", width="100%"),
            rx.select.content(
                rx.foreach(CanvasState.export_sizes, lambda sz: rx.select.item(sz, value=sz))
            ),
            value=CanvasState.selected_export_size,
            on_change=lambda val: setattr(CanvasState, "selected_export_size", val),
            width="100%"
        ),
        rx.cond(
            CanvasState.selected_export_size == "Custom",
            rx.hstack(
                rx.vstack(
                    rx.text("Width (px)", size="1", color_scheme="gray"),
                    rx.input(
                        value=CanvasState.custom_width.to_string(),
                        on_change=lambda val: setattr(CanvasState, "custom_width", int(val) if val.isdigit() else 1024),
                        type="number"
                    ),
                    align_items="start"
                ),
                rx.vstack(
                    rx.text("Height (px)", size="1", color_scheme="gray"),
                    rx.input(
                        value=CanvasState.custom_height.to_string(),
                        on_change=lambda val: setattr(CanvasState, "custom_height", int(val) if val.isdigit() else 1024),
                        type="number"
                    ),
                    align_items="start"
                ),
                spacing="3", width="100%", margin_top="0.5rem"
            )
        ),
        rx.hstack(
            rx.button("Cancel", on_click=lambda: setattr(CanvasState, "show_export_modal", False), variant="soft", color_scheme="gray"),
            rx.button("Confirm Export", on_click=CanvasState.export_canvas, icon="download"),
            spacing="3", justify="end", width="100%", margin_top="1.5rem"
        ),
        spacing="3"
    )

def export_modal_component():
    return modal(
        "Export Canvas",
        _export_modal_content(),
        is_open=CanvasState.show_export_modal,
        on_close=lambda: setattr(CanvasState, "show_export_modal", False),
        size="sm"
    )

def _ab_test_modal_content():
    return rx.vstack(
        rx.cond(
            rx.length(CanvasState.ab_test_results) > 0,
            rx.vstack(
                rx.foreach(
                    CanvasState.ab_test_results,
                    lambda result: card([
                        rx.hstack(
                            rx.image(src=result.get("image_url", "/placeholder/100/100.svg"), class_name="w-20 h-20 object-cover rounded"),
                            rx.vstack(
                                rx.text(result.get("variant_name", "N/A"), weight="bold"),
                                rx.text(rx.text.concat("Score: ", result.get("score_mock", 0).to_string()), size="1", color_scheme="gray"),
                                rx.text(rx.text.concat("Engagement: ", result.get("engagement_mock", 0).to_string()), size="1", color_scheme="gray"),
                                align_items="start", spacing="1"
                            ),
                            spacing="3", align_items="center"
                        )
                    ])
                ),
                spacing="3", max_height="60vh", overflow_y="auto"
            ),
            rx.center(rx.text("No A/B test results to display.", color_scheme="gray"), padding="2rem")
        ),
        spacing="3"
    )

def ab_test_modal_component():
    return modal(
        "A/B Test Results",
        _ab_test_modal_content(),
        is_open=CanvasState.show_ab_test_modal,
        on_close=lambda: setattr(CanvasState, "show_ab_test_modal", False),
        size="md"
    )

def _tutorial_overlay_content():
    tutorial_steps_text = {
        0: "Welcome! Click 'Base Image' in the toolbar to add your first node.",
        1: "Great! Now click 'Style' to add a style node and connect it to the image node.",
        2: "Connect an 'AI Gen' node. Configure its prompt and click 'Generate'!",
        3: "Explore other nodes like 'Text' and 'Filter' to enhance your creation.",
        4: "Use the Live Preview panel to adjust layers directly!"
    }
    current_step_text = tutorial_steps_text.get(CanvasState.tutorial_step, "You're doing great! Keep exploring.")

    return rx.vstack(
        rx.heading(rx.text.concat("Tutorial - Step ", (CanvasState.tutorial_step + 1).to_string()), size="6"),
        rx.text(current_step_text, margin_y="1rem", color_scheme="gray"),
        rx.hstack(
            rx.button("Previous", on_click=CanvasState.prev_tutorial_step, disabled=CanvasState.tutorial_step == 0, variant="soft"),
            rx.button("Next", on_click=CanvasState.next_tutorial_step, icon="arrow-right"),
            rx.flex(grow=1),
            rx.button("End Tutorial", on_click=CanvasState.end_tutorial, variant="outline", color_scheme="gray"),
            spacing="3", width="100%"
        ),
        spacing="4"
    )

def tutorial_overlay_component():
    return rx.cond(
        CanvasState.show_tutorial,
        rx.box(
            rx.box(
                _tutorial_overlay_content(),
                class_name="bg-[var(--color-panel-solid)] border border-[var(--gray-a6)] rounded-lg p-6 max-w-lg shadow-2xl"
            ),
            class_name="fixed inset-0 bg-black/70 flex items-center justify-center z-[100]"
        )
    )

def editor():
    return rx.box(
        export_modal_component(),
        ab_test_modal_component(),
        tutorial_overlay_component(),

        rx.vstack(
            enhanced_toolbar(),
            rx.hstack(
                # Left Sidebar (Properties & Layers)
                rx.vstack(
                    properties_panel(),
                    layers_panel(),
                    spacing="0",
                    width="320px",
                    height="100%",
                    border_right="1px solid var(--gray-a5)"
                ),
                # Main Canvas Area
                enhanced_canvas(),
                # Right Sidebar (AI Assistant & Preview)
                rx.vstack(
                    live_preview_panel(),
                    ai_assistant_panel(),
                    spacing="4",
                    width="320px",
                    height="100%",
                    border_left="1px solid var(--gray-a5)"
                ),
                spacing="0",
                width="100%",
                height="calc(100vh - 70px)",
                align_items="stretch"
            ),
            spacing="0",
            width="100vw",
            height="100vh",
            class_name="bg-[var(--gray-a1)] overflow-hidden flex flex-col"
        )
    )
