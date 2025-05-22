# frontend/components/enhanced_canvas.py
import reflex as rx
from .reactflow import react_flow, background, controls, mini_map
from typing import Dict, Any, List, Optional
from .ui_components import primary_button, icon_button, card, sidebar_panel, color_picker, progress_bar
from ..state.canvas_state import CanvasState

def enhanced_toolbar():
    return rx.hstack(
        # Node Creation Tools
        rx.hstack(
            primary_button("Base Image", CanvasState.add_base_image_node, "image"),
            primary_button("Style", CanvasState.add_style_node, "palette"),
            primary_button("AI Gen", CanvasState.add_ai_processor_node, "cpu"),
            primary_button("Text", CanvasState.add_text_node, "type"),
            primary_button("Filter", CanvasState.add_filter_node, "filter"),
            primary_button("A/B Test", CanvasState.add_ab_test_node, "git-fork"),
            primary_button("Output", CanvasState.add_output_node, "arrow-down-to-line"),
            primary_button("Annotation", CanvasState.add_annotation_node, "pen-square"),
            spacing="2",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700 flex-wrap gap-2"
        ),

        # Selection/View Tools
        rx.hstack(
            icon_button("mouse-pointer-2", tooltip="Select Tool"),
            icon_button("hand", tooltip="Pan Tool"),
            icon_button("zoom-in", on_click=lambda: CanvasState.set_zoom_level(CanvasState.zoom_level + 0.1), tooltip="Zoom In"),
            icon_button("zoom-out", on_click=lambda: CanvasState.set_zoom_level(CanvasState.zoom_level - 0.1), tooltip="Zoom Out"),
            icon_button("grid-3x3", on_click=CanvasState.toggle_grid, tooltip="Toggle Grid"),
            icon_button("ruler", on_click=CanvasState.toggle_rulers, tooltip="Toggle Rulers"),
            icon_button("palette", on_click=CanvasState.toggle_canvas_theme, tooltip="Change Canvas Theme"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Edit Tools
        rx.hstack(
            icon_button("copy", CanvasState.duplicate_selected_nodes, "Duplicate Selected"),
            icon_button("trash-2", CanvasState.delete_selected_nodes, "Delete Selected"),
            icon_button("folder-plus", CanvasState.group_selected_nodes, "Group Selected"),
            icon_button("folder-minus", CanvasState.ungroup_selected_nodes, "Ungroup Selected"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Canvas Actions
        rx.hstack(
            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success"),
            primary_button("Clear All", CanvasState.clear_canvas, "trash", variant="danger"),
            primary_button("Export", lambda: setattr(CanvasState, "show_export_modal", True), "download"),
            spacing="2"
        ),
        spacing="3",
        width="100%",
        padding="0.75rem",
        class_name="bg-gray-900 shadow-lg border-b border-gray-700 flex-wrap justify-start md:justify-between gap-3",
        align_items="center"
    )

def live_preview_panel():
    return rx.box(
        rx.cond(
            CanvasState.preview_image != "",
            rx.vstack(
                rx.image(
                    src=CanvasState.preview_image,
                    class_name="w-full h-64 object-contain rounded-lg"
                ),
                rx.hstack(
                    icon_button("move", tooltip="Move Layer", on_click=CanvasState.start_layer_manipulation),
                    icon_button("text-cursor", tooltip="Edit Text", on_click=CanvasState.edit_preview_text),
                    spacing="2"
                ),
                spacing="2",
                class_name="p-4"
            ),
            rx.text("No preview available", color_scheme="gray", class_name="text-sm")
        ),
        class_name="preview-panel w-80 max-h-[70vh] overflow-y-auto"
    )

def enhanced_canvas():
    return rx.hstack(
        react_flow(
            nodes=CanvasState.nodes,
            edges=CanvasState.edges,
            on_nodes_change=CanvasState.on_nodes_change,
            on_edges_change=lambda changes: setattr(CanvasState, 'edges', CanvasState.edges),
            on_connect=CanvasState.on_connect,
            on_pane_click=CanvasState.deselect_node,
            on_node_click=lambda event, node: CanvasState.select_node(node["id"]),
            fit_view=True,
            nodes_draggable=True,
            nodes_connectable=True,
            elements_selectable=True,
            min_zoom=0.2,
            max_zoom=4.0,
            class_name="w-full flex-1 border border-[var(--gray-a5)] rounded-lg relative bg-[var(--gray-a2)]"
        ),
        background(
            variant=rx.cond(
                CanvasState.canvas_theme == "grid", "lines",
                CanvasState.canvas_theme == "dots", "dots",
                "cross"
            ),
            gap=20,
            size=1,
            color=rx.cond(
                CanvasState.canvas_theme == "gradient",
                "rgba(59, 130, 246, 0.2)",
                "#aaa"
            )
        ),
        controls(),
        mini_map(pannable=True, zoomable=True),

        # Rulers
        rx.cond(
            CanvasState.rulers_enabled,
            rx.fragment(
                rx.box(class_name="absolute top-0 left-8 right-0 h-8 bg-[var(--gray-a3)] border-b border-[var(--gray-a5)] z-[1] pointer-events-none"),
                rx.box(class_name="absolute left-0 top-8 bottom-0 w-8 bg-[var(--gray-a3)] border-r border-[var(--gray-a5)] z-[1] pointer-events-none"),
            )
        ),

        # Selection info
        rx.cond(
            rx.length(CanvasState.selected_nodes) > 0,
            rx.box(
                rx.text(
                    rx.text.concat(rx.length(CanvasState.selected_nodes).to_string(), " node(s) selected"),
                    color_scheme="gray", high_contrast=True, size="1"
                ),
                class_name="absolute bottom-3 left-3 bg-[var(--gray-a3)] px-2 py-1 rounded border border-[var(--gray-a5)] shadow-md z-[2]"
            )
        ),

        # Zoom indicator
        rx.box(
            rx.text(
                rx.text.concat((CanvasState.zoom_level * 100).round().to_string(), "%"),
                color_scheme="gray", high_contrast=True, size="1"
            ),
            class_name="absolute bottom-3 right-3 bg-[var(--gray-a3)] px-2 py-1 rounded border border-[var(--gray-a5)] shadow-md z-[2]"
        ),

        # Spotlight for tutorial
        rx.cond(
            CanvasState.show_tutorial_spotlight,
            rx.box(
                class_name="spotlight",
                style={
                    "width": CanvasState.spotlight_size["width"],
                    "height": CanvasState.spotlight_size["height"],
                    "top": CanvasState.spotlight_size["y"],
                    "left": CanvasState.spotlight_size["x"],
                }
            )
        ),

        class_name="relative flex-1",
        style={"height": "calc(100vh - 70px)"}
    )

def properties_panel_content(node: rx.Var[Dict[str, Any]]):
    def update_node_data(field: str, value: Any):
        CanvasState.update_node_property(node["id"], field, value)

    return rx.vstack(
        card([
            rx.text(rx.text.concat("Node: ", node.get("data", {}).get("label", "N/A")), weight="bold"),
            rx.text(rx.text.concat("ID: ", node.get("id", "N/A")), size="1", color_scheme="gray"),
            rx.text(rx.text.concat("Type: ", node.get("type", "N/A")), size="1", color_scheme="gray"),
            rx.hstack(
                rx.text("Node Color", size="1", color_scheme="gray"),
                color_picker(
                    value=node.get("style", {}).get("background", "#1e40af"),
                    on_change=lambda color: update_node_data("style.background", color)
                ),
                spacing="2"
            ),
            rx.cond(
                node.get("data", {}).get("status") != "idle",
                progress_bar(
                    value=rx.cond(node.get("data", {}).get("status") == "complete", 100, 50),
                    max_value=100,
                    color=rx.cond(node.get("data", {}).get("status") == "complete", "green", "yellow"),
                    show_text=False
                )
            ),
        ], title="Node Information"),

        card([
            rx.hstack(
                rx.vstack(
                    rx.text("X", size="1", color_scheme="gray"),
                    rx.input(
                        value=node.get("position", {}).get("x", 0).to_string(),
                        on_change=lambda val: update_node_data("position.x", float(val)),
                        type="number", placeholder="X", size="1"
                    ),
                ),
                rx.vstack(
                    rx.text("Y", size="1", color_scheme="gray"),
                    rx.input(
                        value=node.get("position", {}).get("y", 0).to_string(),
                        on_change=lambda val: update_node_data("position.y", float(val)),
                        type="number", placeholder="Y", size="1"
                    ),
                ),
                spacing="3",
            )
        ], title="Position"),

        rx.cond(
            node.get("data", {}).get("label", "").contains("AI Generator"),
            card([
                rx.text("Prompt", size="1", color_scheme="gray"),
                rx.text_area(
                    value=node.get("data", {}).get("prompt", ""),
                    on_change=lambda val: update_node_data("prompt", val),
                    placeholder="Enter AI prompt...",
                    rows=3,
                    size="1"
                ),
                rx.hstack(
                    rx.text("Steps", size="1", color_scheme="gray"),
                    rx.slider(
                        value=[node.get("data", {}).get("steps", 50)],
                        min=10, max=150, step=1,
                        on_value_commit=lambda val_list: update_node_data("steps", val_list[0]),
                        flex_grow=1
                    ),
                    spacing="2"
                ),
            ], title="AI Prompt")
        ),

        rx.cond(
            node.get("data", {}).get("label", "").contains("Text Overlay"),
            card([
                rx.text("Text Content", size="1", color_scheme="gray"),
                rx.text_area(
                    value=node.get("data", {}).get("text_content", ""),
                    on_change=lambda val: update_node_data("text_content", val),
                    placeholder="Enter text...",
                    rows=2,
                    size="1"
                ),
                rx.hstack(
                    rx.text("Font Size", size="1", color_scheme="gray"),
                    rx.slider(
                        value=[node.get("data", {}).get("font_size", 24)],
                        min=12, max=72, step=1,
                        on_value_commit=lambda val_list: update_node_data("font_size", val_list[0]),
                        flex_grow=1
                    ),
                    spacing="2"
                ),
            ], title="Text Properties")
        ),

        spacing="4",
        width="100%"
    )

def properties_panel():
    return sidebar_panel(
        "Properties",
        [
            rx.cond(
                CanvasState.selected_node.contains("id"),
                properties_panel_content(CanvasState.selected_node),
                rx.center(
                    rx.text("Select a node to see its properties.", color_scheme="gray", align="center"),
                    height="100%",
                )
            )
        ],
        is_open=CanvasState.show_properties_panel
    )

def layers_panel():
    return sidebar_panel(
        "Layers",
        [
            rx.cond(
                rx.length(CanvasState.nodes) > 0,
                rx.vstack(
                    rx.foreach(
                        CanvasState.nodes,
                        lambda node: rx.hstack(
                            rx.icon(
                                tag=rx.cond(
                                    node.get("type") == "group",
                                    CanvasState.group_collapsed_ids.contains(node.get("id")),
                                    "chevron-right",
                                    "chevron-down"
                                ),
                                size=14,
                                margin_right="0.5em",
                                color_scheme=rx.cond(
                                    CanvasState.selected_node.get("id") == node.get("id"),
                                    "accent",
                                    "gray"
                                ),
                                on_click=rx.cond(
                                    node.get("type") == "group",
                                    lambda: CanvasState.toggle_group_collapse(node.get("id"))
                                )
                            ),
                            rx.icon(
                                tag=CanvasState.get_node_icon(node.get("type")),
                                size=14,
                                margin_right="0.5em",
                                color_scheme=rx.cond(
                                    CanvasState.selected_node.get("id") == node.get("id"),
                                    "accent",
                                    "gray"
                                )
                            ),
                            rx.text(
                                node.get("data", {}).get("label", node.get("id")),
                                size="2",
                                weight=rx.cond(
                                    CanvasState.selected_node.get("id") == node.get("id"),
                                    "bold",
                                    "regular"
                                ),
                                color_scheme=rx.cond(
                                    CanvasState.selected_node.get("id") == node.get("id"),
                                    "accent",
                                    "gray"
                                ),
                                flex_grow=1,
                                truncate=True,
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                            padding="0.3rem 0.5rem",
                            border_radius="var(--radius-2)",
                            _hover={"background_color": "var(--gray-a3)"},
                            background_color=rx.cond(
                                CanvasState.selected_node.get("id") == node.get("id"),
                                "var(--accent-3)",
                                "transparent"
                            ),
                            cursor="pointer",
                            on_click=lambda: CanvasState.select_node(node.get("id"))
                        )
                    ),
                    spacing="1",
                    width="100%",
                    max_height="40vh",
                    overflow_y="auto"
                ),
                rx.center(
                    rx.text("No nodes on canvas.", color_scheme="gray"),
                    height="100%"
                )
            )
        ],
        is_open=CanvasState.show_layers_panel
    )

def ai_assistant_panel():
    _current_suggestions_var = rx.Var.create(CanvasState.generate_prompt_suggestions())

    return card([
        rx.vstack(
            rx.heading("AI Assistant", size="5"),
            rx.text("AI Model", size="1", color_scheme="gray", margin_bottom="0.25rem"),
            rx.select.root(
                rx.select.trigger(placeholder="Select AI Model", width="100%", size="2"),
                rx.select.content(
                    rx.foreach(
                        CanvasState.available_models,
                        lambda model: rx.select.item(model.get("name"), value=model.get("id"))
                    )
                ),
                value=CanvasState.selected_model,
                on_change=lambda val: setattr(CanvasState, "selected_model", val),
                width="100%"
            ),
            rx.hstack(
                rx.text("Prompt Suggestions", size="1", color_scheme="gray", margin_top="1rem"),
                icon_button(
                    "refresh-cw",
                    on_click=lambda: _current_suggestions_var.set(CanvasState.generate_prompt_suggestions()),
                    size="sm",
                    class_name="ml-auto",
                    variant="ghost"
                ),
                width="100%",
                justify="space-between",
                align_items="center"
            ),
            rx.vstack(
                rx.foreach(
                    _current_suggestions_var,
                    lambda suggestion: rx.button(
                        suggestion,
                        variant="outline",
                        color_scheme="gray",
                        width="100%",
                        text_align="left",
                        size="1",
                        class_name="truncate",
                        on_click=lambda: CanvasState.apply_suggestion(suggestion)
                    )
                ),
                spacing="1",
                width="100%",
                margin_top="0.25rem"
            ),
            rx.hstack(
                rx.text("Steps", size="1", color_scheme="gray", margin_top="1rem"),
                rx.slider(
                    value=[CanvasState.model_settings.get("steps", 50)],
                    min=10,
                    max=150,
                    step=1,
                    on_value_commit=lambda val_list: CanvasState.update_model_settings("steps", val_list[0]),
                    flex_grow=1
                ),
                rx.text(
                    CanvasState.model_settings.get("steps", 50).to_string(),
                    size="2",
                    min_width="3em",
                    text_align="right"
                ),
                spacing="3",
                width="100%",
                align_items="center"
            ),
            rx.hstack(
                rx.text("Guidance Scale", size="1", color_scheme="gray", margin_top="1rem"),
                rx.slider(
                    value=[CanvasState.model_settings.get("guidance_scale", 7.5)],
                    min=1,
                    max=20,
                    step=0.1,
                    on_value_commit=lambda val_list: CanvasState.update_model_settings("guidance_scale", val_list[0]),
                    flex_grow=1
                ),
                rx.text(
                    CanvasState.model_settings.get("guidance_scale", 7.5).to_string(),
                    size="2",
                    min_width="3em",
                    text_align="right"
                ),
                spacing="3",
                width="100%",
                align_items="center"
            ),
            primary_button(
                "Generate Image",
                CanvasState.generate_visual,
                "sparkles",
                variant="success",
                class_name="w-full mt-4"
            ),
            rx.vstack(
                rx.text("Workflow Suggestions", size="1", color_scheme="gray", margin_top="1rem"),
                rx.foreach(
                    CanvasState.auto_optimize_workflow(),
                    lambda suggestion: rx.box(
                        rx.text(
                            suggestion.get("message", ""),
                            size="1",
                            color_scheme="gray",
                            class_name="truncate"
                        ),
                        class_name="p-2 bg-[var(--gray-a3)] rounded border border-[var(--gray-a5)]"
                    )
                ),
                spacing="1",
                width="100%"
            ),
            spacing="4"
        )
    ], class_name="w-80 h-full overflow-y-auto p-4")
