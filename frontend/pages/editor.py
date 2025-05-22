import reflex as rx
from ..components.enhanced_canvas import enhanced_toolbar, enhanced_canvas, properties_panel, layers_panel, ai_assistant_panel
from ..components.ui_components import modal, primary_button, card, tabs
from ..state.canvas_state import CanvasState

def export_modal():
    return modal(
        "Export Settings",
        rx.vstack(
            rx.vstack(
                rx.text("Format", color="gray.400", font_size="sm"),
                rx.select(
                    CanvasState.export_formats,
                    value=CanvasState.selected_export_format,
                    on_change=lambda x: setattr(CanvasState, "selected_export_format", x)
                ),
                spacing="2"
            ),
            rx.vstack(
                rx.text("Size", color="gray.400", font_size="sm"),
                rx.select(
                    CanvasState.export_sizes,
                    value=CanvasState.selected_export_size,
                    on_change=lambda x: setattr(CanvasState, "selected_export_size", x)
                ),
                spacing="2"
            ),
            rx.cond(
                CanvasState.selected_export_size == "Custom",
                rx.hstack(
                    rx.vstack(
                        rx.text("Width", color="gray.400", font_size="sm"),
                        rx.number_input(
                            value=CanvasState.custom_width,
                            on_change=lambda x: setattr(CanvasState, "custom_width", x)
                        ),
                        spacing="1"
                    ),
                    rx.vstack(
                        rx.text("Height", color="gray.400", font_size="sm"),
                        rx.number_input(
                            value=CanvasState.custom_height,
                            on_change=lambda x: setattr(CanvasState, "custom_height", x)
                        ),
                        spacing="1"
                    ),
                    spacing="4"
                ),
                rx.box()
            ),
            rx.hstack(
                primary_button("Cancel", lambda: setattr(CanvasState, "show_export_modal", False), variant="secondary"),
                primary_button("Export", CanvasState.export_canvas, "download", variant="success"),
                spacing="3"
            ),
            spacing="6"
        ),
        CanvasState.show_export_modal,
        lambda: setattr(CanvasState, "show_export_modal", False)
    )

def ab_test_modal():
    return modal(
        "A/B Test Results",
        rx.vstack(
            rx.cond(
                CanvasState.ab_test_results,
                rx.vstack(
                    rx.foreach(
                        CanvasState.ab_test_results,
                        lambda result, index: card([
                            rx.hstack(
                                rx.image(
                                    src=result.get("image_url", "/api/placeholder/100/100"),
                                    class_name="w-24 h-24 object-cover rounded"
                                ),
                                rx.vstack(
                                    rx.text(result.get("variant", ""), color="white", font_weight="bold"),
                                    rx.text(f"Score: {result.get('score', 0)}/100", color="gray.400"),
                                    rx.text(f"Engagement: {result.get('engagement', 0)}", color="gray.400"),
                                    rx.text(f"Conversion: {result.get('conversion', 0)}%", color="gray.400"),
                                    align="start",
                                    spacing="1"
                                ),
                                spacing="4",
                                align="center"
                            )
                        ])
                    ),
                    spacing="4"
                ),
                rx.text("No A/B test results available", color="gray.400")
            ),
            spacing="4"
        ),
        rx.Var.create(len(CanvasState.ab_test_results) > 0, _var_is_local=False),
        lambda: setattr(CanvasState, "ab_test_results", [])
    )

def tutorial_overlay():
    return rx.cond(
        CanvasState.show_tutorial,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading(f"Tutorial Step {CanvasState.tutorial_step + 1}", size="lg", color="white"),
                    rx.text("Welcome to the AI Visual Generator! Let's start by adding your first node.", 
                           color="gray.300"),
                    rx.hstack(
                        primary_button("Previous", CanvasState.prev_tutorial_step, disabled=CanvasState.tutorial_step == 0),
                        primary_button("Next", CanvasState.next_tutorial_step),
                        primary_button("Skip", CanvasState.end_tutorial, variant="secondary"),
                        spacing="3"
                    ),
                    spacing="4"
                ),
                class_name="bg-gray-800 border border-gray-600 rounded-lg p-6 max-w-md"
            ),
            class_name="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        ),
        rx.box()
    )

def editor():
    return rx.box(
        # Modals
        export_modal(),
        ab_test_modal(),
        tutorial_overlay(),
        
        # Main Layout
        rx.vstack(
            enhanced_toolbar(),
            
            rx.hstack(
                # Left Sidebar
                rx.hstack(
                    layers_panel(),
                    properties_panel(),
                    spacing="0"
                ),
                
                # Main Canvas Area
                enhanced_canvas(),
                
                # Right Sidebar - AI Assistant
                ai_assistant_panel(),
                
                spacing="0",
                class_name="flex-1"
            ),
            
            spacing="0"
        ),
        
        class_name="h-screen bg-gray-900 overflow-hidden"
    )
