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
            primary_button("AI Generator", CanvasState.add_ai_processor_node, "cpu"),
            primary_button("Text", CanvasState.add_text_node, "type"),
            primary_button("Filter", CanvasState.add_filter_node, "filter"),
            primary_button("A/B Test", CanvasState.add_ab_test_node, "split"),
            spacing="2",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),
        
        # Selection Tools
        rx.hstack(
            icon_button("move", tooltip="Select"),
            icon_button("hand", tooltip="Pan"),
            icon_button("zoom-in", tooltip="Zoom In"),
            icon_button("zoom-out", tooltip="Zoom Out"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),
        
        # Edit Tools
        rx.hstack(
            icon_button("copy", CanvasState.duplicate_selected_nodes, "Duplicate"),
            icon_button("trash", CanvasState.delete_selected_nodes, "Delete"),
            icon_button("folder", CanvasState.group_selected_nodes, "Group"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),
        
        # View Options
        rx.hstack(
            icon_button("grid-3x3", CanvasState.toggle_grid, "Toggle Grid"),
            icon_button("rulers", CanvasState.toggle_rulers, "Toggle Rulers"),
            icon_button("eye", tooltip="View Mode"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),
        
        # Canvas Actions
        rx.hstack(
            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success"),
            primary_button("Clear", CanvasState.clear_canvas, "trash", variant="danger"),
            primary_button("Export", lambda: setattr(CanvasState, "show_export_modal", True), "download"),
            spacing="2"
        ),
        
        spacing="4",
        width="100%",
        padding="1rem",
        class_name="bg-gray-900 shadow-lg border-b border-gray-700",
        justify="space-between"
    )

def enhanced_canvas():
    return rx.box(
        react_flow(
            background(
                variant="dots" if CanvasState.grid_enabled else "cross",
                color=CanvasState.theme_background,
                gap=20,
                size=1
            ),
            controls(
                show_zoom=True,
                show_fit_view=True,
                show_interactive=True
            ),
            mini_map(
                node_color=CanvasState.accent_color,
                mask_color="#1f2937",
                zoomable=True,
                pannable=True
            ),
            nodes=CanvasState.nodes,
            edges=CanvasState.edges,
            nodes_draggable=True,
            nodes_connectable=True,
            fit_view=True,
            min_zoom=0.1,
            max_zoom=5.0,
            default_viewport={"x": 0, "y": 0, "zoom": CanvasState.zoom_level},
            on_connect=CanvasState.on_connect,
            on_nodes_change=CanvasState.on_nodes_change,
            on_pane_click=CanvasState.deselect_node,
            style={
                "background": rx.cond(
                    CanvasState.theme == "dark", 
                    "linear-gradient(135deg, #1f2937 0%, #111827 100%)",
                    "linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%)"
                )
            },
            class_name="w-full flex-1 border border-gray-700 rounded-lg relative"
        ),
        
        # Rulers (conditional)
        rx.cond(
            CanvasState.rulers_enabled,
            rx.box(
                # Top ruler
                rx.box(
                    class_name="absolute top-0 left-8 right-0 h-8 bg-gray-800 border-b border-gray-600"
                ),
                # Left ruler  
                rx.box(
                    class_name="absolute left-0 top-8 bottom-0 w-8 bg-gray-800 border-r border-gray-600"
                ),
                class_name="absolute inset-0 pointer-events-none"
            ),
            rx.box()
        ),
        
        # Selection info
        rx.cond(
            CanvasState.selected_nodes,
            rx.box(
                rx.text(f"{len(CanvasState.selected_nodes)} node(s) selected", 
                       color="white", font_size="sm"),
                class_name="absolute bottom-4 left-4 bg-gray-800 px-3 py-2 rounded border border-gray-600"
            ),
            rx.box()
        ),
        
        # Zoom indicator
        rx.box(
            rx.text(f"{int(CanvasState.zoom_level * 100)}%", 
                   color="white", font_size="sm"),
            class_name="absolute bottom-4 right-4 bg-gray-800 px-3 py-2 rounded border border-gray-600"
        ),
        
        class_name="relative flex-1",
        style={"height": "calc(100vh - 140px)"}
    )

def properties_panel():
    return sidebar_panel(
        "Properties",
        [
            rx.cond(
                CanvasState.selected_node,
                rx.vstack(
                    # Node Info
                    card([
                        rx.text(f"Node: {CanvasState.selected_node.get('data', {}).get('label', 'Unknown')}", 
                               color="white", font_weight="bold"),
                        rx.text(f"ID: {CanvasState.selected_node.get('id', '')}", 
                               color="gray.400", font_size="sm"),
                        rx.text(f"Type: {CanvasState.selected_node.get('type', '')}", 
                               color="gray.400", font_size="sm"),
                    ], "Node Information"),
                    
                    # Position Controls
                    card([
                        rx.hstack(
                            rx.vstack(
                                rx.text("X", color="gray.400", font_size="sm"),
                                rx.number_input(
                                    value=CanvasState.selected_node.get("position", {}).get("x", 0),
                                    class_name="w-20"
                                ),
                                spacing="1"
                            ),
                            rx.vstack(
                                rx.text("Y", color="gray.400", font_size="sm"),
                                rx.number_input(
                                    value=CanvasState.selected_node.get("position", {}).get("y", 0),
                                    class_name="w-20"
                                ),
                                spacing="1"
                            ),
                            spacing="4"
                        )
                    ], "Position"),
                    
                    # Style Controls
                    card([
                        rx.vstack(
                            rx.select(
                                CanvasState.available_styles,
                                value=CanvasState.current_style,
                                on_change=CanvasState.set_global_style,
                                class_name="w-full"
                            ),
                            rx.slider(
                                min=0,
                                max=1,
                                step=0.1,
                                value=0.7,
                                class_name="w-full"
                            ),
                            spacing="3"
                        )
                    ], "Style Settings"),
                    
                    spacing="4"
                ),
                
                # No Selection State
                rx.box(
                    rx.text("Select a node to edit properties", 
                           color="gray.400", text_align="center"),
                    class_name="h-full flex items-center justify-center"
                )
            )
        ],
        CanvasState.show_context_menu  # This would need to be a proper state var
    )

def layers_panel():
    return sidebar_panel(
        "Layers",
        [
            rx.vstack(
                rx.foreach(
                    CanvasState.nodes,
                    lambda node, index: rx.hstack(
                        rx.icon(tag="square", size=16, color="blue.500"),
                        rx.text(node["data"].get("label", f"Node {node['id']}"), 
                               color="white", flex="1"),
                        icon_button("eye", size="sm"),
                        icon_button("lock", size="sm"),
                        spacing="2",
                        width="100%",
                        class_name="bg-gray-700 hover:bg-gray-600 px-3 py-2 rounded cursor-pointer",
                        on_click=lambda node=node: CanvasState.select_node(node["id"])
                    )
                ),
                spacing="1",
                width="100%"
            )
        ]
    )

def ai_assistant_panel():
    return card([
        rx.vstack(
            rx.heading("AI Assistant", size="md", color="white"),
            
            # Model Selection
            rx.vstack(
                rx.text("AI Model", color="gray.400", font_size="sm"),
                rx.select(
                    [model["name"] for model in CanvasState.available_models],
                    value=next((m["name"] for m in CanvasState.available_models 
                              if m["id"] == CanvasState.selected_model), "DALL-E 3"),
                    class_name="w-full"
                ),
                spacing="2"
            ),
            
            # Prompt Suggestions
            rx.vstack(
                rx.text("Prompt Suggestions", color="gray.400", font_size="sm"),
                rx.vstack(
                    *[
                        rx.button(
                            suggestion,
                            class_name="w-full text-left text-sm bg-gray-700 hover:bg-gray-600 text-gray-200 p-2 rounded",
                            on_click=lambda s=suggestion: None  # Set prompt
                        )
                        for suggestion in CanvasState.generate_prompt_suggestions()[:3]
                    ],
                    spacing="1"
                ),
                spacing="2"
            ),
            
            # Generation Settings
            rx.vstack(
                rx.text("Quality Settings", color="gray.400", font_size="sm"),
                rx.vstack(
                    rx.hstack(
                        rx.text("Steps:", color="gray.400", font_size="sm"),
                        rx.text(str(CanvasState.model_settings.get("steps", 50)), color="white", font_size="sm"),
                        justify="space-between"
                    ),
                    rx.slider(
                        min=10,
                        max=100,
                        value=CanvasState.model_settings.get("steps", 50),
                        class_name="w-full"
                    ),
                    spacing="2"
                ),
                spacing="2"
            ),
            
            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success"),
            
            spacing="4"
        )
    ], className="h-fit")
