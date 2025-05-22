import reflex as rx
from .reactflow import react_flow, background, controls, mini_map
from ..state.canvas_state import CanvasState
from .ui_components import primary_button, modal
from .collaboration import collaboration_panel

def canvas_toolbar():
    return rx.hstack(
        primary_button("Add Base Image", CanvasState.add_base_image_node, icon="image"),
        primary_button("Add Secondary Image", CanvasState.add_secondary_image_node, icon="plus-circle"),
        primary_button("Add Style Node", CanvasState.add_style_node, icon="palette"),
        primary_button("Add AI Processor", CanvasState.add_ai_processor_node, icon="cpu"),
        primary_button("Add A/B Test Node", CanvasState.add_ab_test_node, icon="split"),
        primary_button("Load Template", CanvasState.show_template_selector, icon="template"),
        primary_button("Start Tutorial", CanvasState.start_tutorial, icon="book-open"),
        primary_button("Export Canvas", CanvasState.export_canvas, icon="download"),
        primary_button("Clear Canvas", CanvasState.clear_canvas, icon="trash"),
        primary_button("Toggle Theme", CanvasState.toggle_theme, icon="moon"),
        spacing="4",
        width="100%",
        padding="1rem",
        class_name="bg-gray-800 shadow-md rounded-lg",
    )

def context_menu():
    return modal(
        title="Node Actions",
        content=rx.vstack(
            primary_button("Duplicate Node", CanvasState.duplicate_node, icon="copy"),
            primary_button("Delete Node", CanvasState.delete_node, icon="trash"),
            primary_button("Group Nodes", CanvasState.group_nodes, icon="folder"),
            primary_button("Customize Node", CanvasState.customize_node, icon="paint-brush"),
            spacing="2",
        ),
        is_open=CanvasState.show_context_menu,
        on_close=CanvasState.close_context_menu,
    )

def template_selector_modal():
    return modal(
        title="Select Template",
        content=rx.vstack(
            rx.select(
                ["Social Media Post", "Ad Banner", "Branding Kit"],
                value=CanvasState.selected_template,
                on_change=CanvasState.load_template,
                class_name="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-200",
            ),
            primary_button("Load", CanvasState.load_template_confirm, icon="check"),
            spacing="2",
        ),
        is_open=CanvasState.show_template_selector,
        on_close=CanvasState.close_template_selector,
    )

def canvas():
    return rx.box(
        react_flow(
            background(variant="cross", color=CanvasState.theme_background, gap=20, size=1),
            controls(show_zoom=True, show_fit_view=True, show_interactive=True),
            mini_map(node_color=CanvasState.accent_color, mask_color="#1f2937", zoomable=True, pannable=True),
            nodes=CanvasState.nodes,
            edges=CanvasState.edges,
            nodes_draggable=True,
            nodes_connectable=True,
            fit_view=True,
            min_zoom=0.2,
            max_zoom=2.0,
            default_viewport={"x": 0, "y": 0, "zoom": 1},
            on_connect=CanvasState.on_connect,
            on_nodes_change=CanvasState.on_nodes_change,
            on_pane_click=CanvasState.deselect_node,
            on_node_context_menu=CanvasState.open_context_menu,
            on_nodes_delete=CanvasState.delete_node,
            on_node_resize=CanvasState.resize_node,
            edge_types={"style": {"stroke": "#9333ea"}, "image": {"stroke": "#3b82f6"}, "test": {"stroke": "#f97316"}},
            style={"background": rx.cond(CanvasState.theme == "dark", "#1f2937", "#f9fafb")},
            class_name="w-full h-[70vh] border-2 border-gray-700 rounded-lg",
            aria_label="Drag-and-drop canvas for visual design",
        ),
        context_menu(),
        template_selector_modal(),
        collaboration_panel(),
        class_name="w-full",
    )
