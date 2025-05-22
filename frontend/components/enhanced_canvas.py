# frontend/components/enhanced_canvas.py
import reflex as rx
from .reactflow import react_flow, background, controls, mini_map
from .ui_components import primary_button, icon_button, card, sidebar_panel
from ..state.canvas_state import CanvasState

def enhanced_toolbar():
    return rx.hstack(
        # Node Creation Tools
        rx.hstack(
            primary_button("Base Image", CanvasState.add_base_image_node, "image"),
            primary_button("Style", CanvasState.add_style_node, "palette"),
            primary_button("AI Gen", CanvasState.add_ai_processor_node, "cpu"), # Shorter name
            primary_button("Text", CanvasState.add_text_node, "type"),
            primary_button("Filter", CanvasState.add_filter_node, "filter"),
            primary_button("A/B Test", CanvasState.add_ab_test_node, "git-fork"), # Changed icon
            spacing="2",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700 flex-wrap" # Added flex-wrap
        ),

        # Selection Tools
        rx.hstack(
            icon_button("mouse-pointer-2", tooltip="Select"), # Lucide icon
            icon_button("hand", tooltip="Pan"),
            icon_button("zoom-in", tooltip="Zoom In"),
            icon_button("zoom-out", tooltip="Zoom Out"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Edit Tools
        rx.hstack(
            icon_button("copy", CanvasState.duplicate_selected_nodes, "Duplicate"),
            icon_button("trash-2", CanvasState.delete_selected_nodes, "Delete"), # Lucide trash-2
            icon_button("folder-plus", CanvasState.group_selected_nodes, "Group"), # Lucide folder-plus
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # View Options
        rx.hstack(
            icon_button("grid-3x3", CanvasState.toggle_grid, "Toggle Grid"),
            icon_button("ruler", CanvasState.toggle_rulers, "Toggle Rulers"), # Lucide ruler
            icon_button("eye", tooltip="View Mode"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Canvas Actions
        rx.hstack(
            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success"),
            primary_button("Clear", CanvasState.clear_canvas, "trash-2", variant="danger"),
            primary_button("Export", lambda: setattr(CanvasState, "show_export_modal", True), "download"),
            spacing="2"
        ),

        spacing="3", # Reduced spacing
        width="100%",
        padding="0.75rem", # Reduced padding
        class_name="bg-gray-900 shadow-lg border-b border-gray-700 flex-wrap justify-start md:justify-between", # Added flex-wrap and responsive justify
        align_items="center"
    )

def enhanced_canvas():
    return rx.box(
        react_flow(
            background(
                variant=rx.cond(CanvasState.grid_enabled, "dots", "cross"), # Conditional variant
                # color=CanvasState.theme_background, # Let ReactFlow handle default based on theme
                gap=20,
                size=1
            ),
            controls(
                show_zoom=True,
                show_fit_view=True,
                show_interactive=True,
                # position="bottom-left" # Example position
            ),
            mini_map(
                node_color=CanvasState.accent_color, # This should work if ReactFlow supports it directly
                # mask_color="#1f2937", # Let ReactFlow handle default
                zoomable=True,
                pannable=True,
                # position="bottom-right" # Example position
            ),
            nodes=CanvasState.nodes,
            edges=CanvasState.edges,
            nodes_draggable=True,
            nodes_connectable=True,
            fit_view=True,
            min_zoom=0.1,
            max_zoom=5.0,
            # default_viewport={"x": 0, "y": 0, "zoom": CanvasState.zoom_level}, # Let fit_view handle initial
            on_connect=CanvasState.on_connect,
            on_nodes_change=CanvasState.on_nodes_change,
            on_pane_click=CanvasState.deselect_node,
            # style={ # React Flow handles its own theme styles usually
            #     "background": rx.cond(
            #         CanvasState.theme == "dark",
            #         "var(--color-page-background)", # Use Radix theme var
            #         "var(--color-page-background)"
            #     )
            # },
            class_name="w-full flex-1 border border-gray-700 rounded-lg relative"
        ),

        # Rulers (conditional)
        rx.cond(
            CanvasState.rulers_enabled,
            rx.box(
                # Top ruler
                rx.box(
                    class_name="absolute top-0 left-8 right-0 h-8 bg-gray-800 border-b border-gray-600 z-10" # Added z-index
                ),
                # Left ruler
                rx.box(
                    class_name="absolute left-0 top-8 bottom-0 w-8 bg-gray-800 border-r border-gray-600 z-10" # Added z-index
                ),
                class_name="absolute inset-0 pointer-events-none"
            ),
            rx.box()
        ),

        # Selection info
        rx.cond(
            CanvasState.selected_nodes, # This might need to be len(CanvasState.selected_nodes) > 0
            rx.box(
                rx.text(f"{rx.length(CanvasState.selected_nodes)} node(s) selected", # Use rx.length for list in UI
                       class_name="text-white text-xs"), # smaller text
                class_name="absolute bottom-4 left-4 bg-gray-800 px-3 py-1.5 rounded border border-gray-600 shadow-md z-10" # Adjusted padding and added shadow, z-index
            ),
            rx.box()
        ),

        # Zoom indicator
        rx.box(
            rx.text(f"{rx.Var.create(CanvasState.zoom_level * 100).round()}%", # Use Var for dynamic updates
                   class_name="text-white text-xs"),
            class_name="absolute bottom-4 right-4 bg-gray-800 px-3 py-1.5 rounded border border-gray-600 shadow-md z-10" # Adjusted padding
        ),

        class_name="relative flex-1",
        style={"height": "calc(100vh - 100px)"} # Adjusted height based on toolbar
    )

def properties_panel():
    # Ensure set_global_style exists or remove/comment out its usage
    # Example: def set_global_style(self, style: str): self.current_style = style (in CanvasState)

    return sidebar_panel(
        "Properties",
        [
            rx.cond(
                CanvasState.selected_node.contains("id"), # Check if selected_node is not empty
                rx.vstack(
                    # Node Info
                    card([
                        rx.text(f"Node: {CanvasState.selected_node.get('data', {}).get('label', 'Unknown')}",
                               class_name="text-white font-bold"),
                        rx.text(f"ID: {CanvasState.selected_node.get('id', '')}",
                               color_scheme="gray", class_name="text-xs"),
                        rx.text(f"Type: {CanvasState.selected_node.get('type', '')}",
                               color_scheme="gray", class_name="text-xs"),
                    ], title="Node Information"),

                    # Position Controls
                    card([
                        rx.hstack(
                            rx.vstack(
                                rx.text("X", color_scheme="gray", class_name="text-xs"),
                                rx.number_input( # This might need to be rx.input(type="number") or a Radix NumberField
                                    value=str(CanvasState.selected_node.get("position", {}).get("x", 0)), # Value as string
                                    # on_change=lambda val: CanvasState.update_node_position(CanvasState.selected_node['id'], 'x', val),
                                    class_name="w-20",
                                    type="number"
                                ),
                                spacing="1"
                            ),
                            rx.vstack(
                                rx.text("Y", color_scheme="gray", class_name="text-xs"),
                                rx.number_input(
                                    value=str(CanvasState.selected_node.get("position", {}).get("y", 0)),
                                    # on_change=lambda val: CanvasState.update_node_position(CanvasState.selected_node['id'], 'y', val),
                                    class_name="w-20",
                                    type="number"
                                ),
                                spacing="1"
                            ),
                            spacing="4"
                        )
                    ], title="Position"),

                    # Style Controls (Example, assuming set_global_style exists)
                    card([
                        rx.vstack(
                            rx.select(
                                CanvasState.available_styles,
                                value=CanvasState.current_style,
                                # on_change=CanvasState.set_global_style, # Make sure this method exists
                                on_change=lambda style: setattr(CanvasState, "current_style", style),
                                width="100%",
                                size="2"
                            ),
                            rx.slider( # Radix Slider
                                default_value=[70], # Value as list
                                min=0,
                                max=100, # Assuming 0-100 scale for intensity
                                step=10,
                                # on_value_change=lambda val: CanvasState.set_style_intensity(val[0] / 100),
                                width="100%"
                            ),
                            spacing="3"
                        )
                    ], title="Style Settings"),

                    spacing="4"
                ),

                # No Selection State
                rx.box(
                    rx.text("Select a node to edit properties",
                           color_scheme="gray", text_align="center", class_name="italic"),
                    class_name="h-full flex items-center justify-center p-4"
                )
            )
        ],
        is_open=CanvasState.show_properties_panel if hasattr(CanvasState, 'show_properties_panel') else rx.Var.create(True) # Ensure state var exists
    )

def layers_panel():
    return sidebar_panel(
        "Layers",
        [
            rx.vstack(
                rx.foreach(
                    CanvasState.nodes,
                    lambda node: rx.hstack( # Removed index as it's not used in lambda
                        rx.icon(tag="square", size=16, color_scheme="blue"),
                        rx.text(node.get("data", {}).get("label", f"Node {node.get('id', '')}"),
                               class_name="text-white flex-1 truncate", # Added truncate
                               color_scheme= rx.cond(CanvasState.selected_node.get("id") == node.get("id"), "blue", "gray")
                        ),
                        icon_button("eye", size="sm", class_name="ml-auto"), # Ensure proper spacing
                        icon_button("lock", size="sm"),
                        spacing="2",
                        width="100%",
                        class_name="bg-gray-700 hover:bg-gray-600 px-3 py-2 rounded cursor-pointer",
                        on_click=lambda: CanvasState.select_node(node.get("id", "")) # Direct call
                    )
                ),
                spacing="1",
                width="100%"
            )
        ],
        is_open=CanvasState.show_layers_panel if hasattr(CanvasState, 'show_layers_panel') else rx.Var.create(True) # Ensure state var exists
    )


def ai_assistant_panel():
    # Simplified prompt suggestions logic for UI
    _current_suggestions = rx.Var.create(CanvasState.generate_prompt_suggestions()[:3])

    return card([
        rx.vstack(
            rx.heading("AI Assistant", size="5", class_name="text-white"), # Radix size

            # Model Selection
            rx.vstack(
                rx.text("AI Model", color_scheme="gray", class_name="text-sm"),
                rx.select(
                    [(model["name"], model["id"]) for model in CanvasState.available_models], # items as (label, value)
                    value=CanvasState.selected_model,
                    on_change=lambda val: setattr(CanvasState, "selected_model", val),
                    width="100%",
                    size="2"
                ),
                spacing="2"
            ),

            # Prompt Suggestions
            rx.vstack(
                rx.hstack(
                    rx.text("Prompt Suggestions", color_scheme="gray", class_name="text-sm"),
                    icon_button("refresh-cw", on_click=lambda: _current_suggestions.set(CanvasState.generate_prompt_suggestions()[:3]), size="sm", class_name="ml-auto"),
                    justify="space-between",
                    width="100%"
                ),
                rx.vstack(
                    rx.foreach(
                        _current_suggestions,
                        lambda suggestion: rx.button(
                            suggestion,
                            variant="soft", # Radix button variant
                            color_scheme="gray",
                            width="100%",
                            text_align="left",
                            class_name="text-sm p-2",
                            on_click=lambda: print(f"Prompt selected: {suggestion}") # Placeholder action
                        )
                    ),
                    spacing="1"
                ),
                spacing="2"
            ),

            # Generation Settings
            rx.vstack(
                rx.text("Quality Settings", color_scheme="gray", class_name="text-sm"),
                rx.vstack(
                    rx.hstack(
                        rx.text("Steps:", color_scheme="gray", class_name="text-sm"),
                        rx.text(str(CanvasState.model_settings.get("steps", 50)), class_name="text-white text-sm"),
                        justify="space-between",
                        width="100%"
                    ),
                    rx.slider(
                        default_value=[CanvasState.model_settings.get("steps", 50)],
                        min=10,
                        max=100,
                        # on_value_change=lambda val: CanvasState.update_model_settings("steps", val[0]),
                        on_value_commit=lambda val: setattr(CanvasState.model_settings, "steps", val[0]), # Update on commit
                        width="100%"
                    ),
                    spacing="2"
                ),
                spacing="2"
            ),

            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success", class_name="w-full mt-2"),

            spacing="4"
        )
    ], class_name="h-fit w-80") # Fixed width for right sidebar
