# frontend/pages/editor.py
import reflex as rx
from ..components.enhanced_canvas import enhanced_toolbar, enhanced_canvas, properties_panel, layers_panel, ai_assistant_panel
from ..components.ui_components import modal, primary_button, card # Removed tabs as it's not used here
from ..state.canvas_state import CanvasState

def export_modal_content(): # Separate content for clarity
    return rx.vstack(
        rx.vstack(
            rx.text("Format", color_scheme="gray", class_name="text-sm"),
            rx.select(
                CanvasState.export_formats,
                value=CanvasState.selected_export_format,
                on_change=lambda x: setattr(CanvasState, "selected_export_format", x),
                width="100%",
                size="2"
            ),
            spacing="2"
        ),
        rx.vstack(
            rx.text("Size", color_scheme="gray", class_name="text-sm"),
            rx.select(
                CanvasState.export_sizes,
                value=CanvasState.selected_export_size,
                on_change=lambda x: setattr(CanvasState, "selected_export_size", x),
                width="100%",
                size="2"
            ),
            spacing="2"
        ),
        rx.cond(
            CanvasState.selected_export_size == "Custom",
            rx.hstack(
                rx.vstack(
                    rx.text("Width", color_scheme="gray", class_name="text-xs"),
                    rx.input( # Changed to rx.input
                        value=str(CanvasState.custom_width),
                        on_change=lambda x: setattr(CanvasState, "custom_width", int(x) if x.isdigit() else CanvasState.custom_width),
                        type="number",
                        placeholder="px"
                    ),
                    spacing="1"
                ),
                rx.vstack(
                    rx.text("Height", color_scheme="gray", class_name="text-xs"),
                    rx.input(
                        value=str(CanvasState.custom_height),
                        on_change=lambda x: setattr(CanvasState, "custom_height", int(x) if x.isdigit() else CanvasState.custom_height),
                        type="number",
                        placeholder="px"
                    ),
                    spacing="1"
                ),
                spacing="4",
                width="100%",
                justify="space-between"
            ),
            rx.box()
        ),
        rx.hstack(
            primary_button("Cancel", lambda: setattr(CanvasState, "show_export_modal", False), variant="secondary"),
            primary_button("Export", CanvasState.export_canvas, "download", variant="success"),
            spacing="3",
            width="100%",
            justify_content="flex-end", # Align buttons to right
            padding_top="1rem"
        ),
        spacing="4" # Reduced spacing
    )

def export_modal_component(): # Renamed to avoid conflict
    return modal(
        "Export Settings",
        export_modal_content(),
        CanvasState.show_export_modal,
        lambda: setattr(CanvasState, "show_export_modal", False),
        size="sm" # Smaller modal
    )

def ab_test_modal_content():
    return rx.vstack(
            rx.cond(
                rx.length(CanvasState.ab_test_results) > 0, # Use rx.length
                rx.vstack(
                    rx.foreach(
                        CanvasState.ab_test_results,
                        lambda result: card([ # Removed index
                            rx.hstack(
                                rx.image(
                                    src=result.get("image_url", "/api/placeholder/100/100"),
                                    class_name="w-24 h-24 object-cover rounded"
                                ),
                                rx.vstack(
                                    rx.text(result.get("variant", ""), class_name="text-white font-bold"),
                                    rx.text(f"Score: {result.get('score', 0)}/100", color_scheme="gray", class_name="text-sm"),
                                    rx.text(f"Engagement: {result.get('engagement', 0)}", color_scheme="gray", class_name="text-sm"),
                                    rx.text(f"Conversion: {result.get('conversion', 0.0):.1f}%", color_scheme="gray", class_name="text-sm"),
                                    align="start",
                                    spacing="1"
                                ),
                                spacing="4",
                                align="center"
                            )
                        ])
                    ),
                    spacing="3", # Reduced spacing
                    max_height="60vh", # Max height for scroll
                    overflow_y="auto"
                ),
                rx.text("No A/B test results available.", color_scheme="gray", class_name="p-4 text-center italic")
            ),
            spacing="3" # Reduced spacing
        )

def ab_test_modal_component(): # Renamed
    return modal(
        "A/B Test Results",
        ab_test_modal_content(),
        CanvasState.show_ab_test_modal if hasattr(CanvasState, 'show_ab_test_modal') else rx.Var.create(False), # Ensure state var exists
        lambda: setattr(CanvasState, "show_ab_test_modal", False) if hasattr(CanvasState, 'show_ab_test_modal') else None,
        size="md"
    )


def tutorial_overlay_content():
    # Example tutorial content, you'd fetch this from CanvasState.get_current_tutorial_text() or similar
    tutorial_texts = [
        "Welcome! Add a 'Base Image' node to start.",
        "Now, connect a 'Style' node to define the look.",
        "Great! Add an 'AI Generator' node and connect it.",
        "Configure the AI Generator and hit 'Generate'!",
    ]
    current_text = rx.Var.create(tutorial_texts[0]) # Default to first
    # This logic would be more complex in CanvasState to get text for current_tutorial_step

    return rx.vstack(
            rx.heading(f"Tutorial: Step {CanvasState.tutorial_step + 1}", size="6", class_name="text-white"),
            rx.text(
                tutorial_texts[CanvasState.tutorial_step] if CanvasState.tutorial_step < len(tutorial_texts) else "Tutorial Complete!",
                color_scheme="gray", class_name="my-3"
            ),
            rx.hstack(
                primary_button("Previous", CanvasState.prev_tutorial_step, disabled=CanvasState.tutorial_step == 0, variant="secondary"),
                primary_button("Next", CanvasState.next_tutorial_step, variant="primary"),
                primary_button("Skip Tutorial", CanvasState.end_tutorial, variant="outline", class_name="ml-auto"),
                spacing="3",
                width="100%",
                justify_content="space-between"
            ),
            spacing="4"
        )

def tutorial_overlay_component(): # Renamed
    return rx.cond(
        CanvasState.show_tutorial,
        rx.box( # Outer box for positioning
            rx.box( # Inner box for styling
                tutorial_overlay_content(),
                class_name="bg-gray-800 border border-gray-600 rounded-lg p-6 max-w-md shadow-2xl"
            ),
            class_name="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-[90]" # Slightly lower z-index than modals
        ),
        rx.box()
    )


def editor():
    # Initialize missing state vars if they are used for UI control and not present
    if not hasattr(CanvasState, 'show_properties_panel'):
        CanvasState.show_properties_panel = rx.Var.create(True)
    if not hasattr(CanvasState, 'show_layers_panel'):
        CanvasState.show_layers_panel = rx.Var.create(True)
    if not hasattr(CanvasState, 'show_ab_test_modal'):
        CanvasState.show_ab_test_modal = rx.Var.create(False)
    if not hasattr(CanvasState, 'active_settings_tab'): # For settings page, but good practice
        CanvasState.active_settings_tab = rx.Var.create("general")


    return rx.box(
        # Modals
        export_modal_component(),
        ab_test_modal_component(),
        tutorial_overlay_component(),

        # Main Layout
        rx.vstack(
            enhanced_toolbar(),

            rx.hstack(
                # Left Sidebar (collapsible example)
                rx.box(
                    rx.hstack(
                        layers_panel(),
                        properties_panel(),
                        spacing="0"
                    ),
                    # class_name=rx.cond(CanvasState.left_sidebar_open, "w-[640px]", "w-12"), # Example for collapsible
                    class_name="transition-width duration-300"
                ),

                # Main Canvas Area
                enhanced_canvas(),

                # Right Sidebar - AI Assistant (fixed width)
                ai_assistant_panel(),

                spacing="0",
                class_name="flex-1 h-[calc(100vh-60px)]" # Adjust height considering toolbar
            ),

            spacing="0",
            class_name="h-screen w-screen bg-gray-900 overflow-hidden flex flex-col" # Ensure full screen and flex col
        )
    )
