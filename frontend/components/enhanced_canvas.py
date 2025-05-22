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
            primary_button("AI Gen", CanvasState.add_ai_processor_node, "cpu"),
            primary_button("Text", CanvasState.add_text_node, "type"), # 'type' for text
            primary_button("Filter", CanvasState.add_filter_node, "filter"),
            primary_button("A/B Test", CanvasState.add_ab_test_node, "git-fork"), # Consistent icon
            primary_button("Output", CanvasState.add_output_node, "arrow-down-to-line"), # Added output node button
            spacing="2",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700 flex-wrap gap-2" # Added gap
        ),

        # Selection/View Tools
        rx.hstack(
            icon_button("mouse-pointer-2", tooltip="Select Tool"),
            icon_button("hand", tooltip="Pan Tool (ReactFlow built-in)"),
            icon_button("zoom-in", on_click=lambda: CanvasState.set_zoom_level(CanvasState.zoom_level + 0.1), tooltip="Zoom In"),
            icon_button("zoom-out", on_click=lambda: CanvasState.set_zoom_level(CanvasState.zoom_level - 0.1), tooltip="Zoom Out"),
            icon_button("grid-3x3", on_click=CanvasState.toggle_grid, tooltip="Toggle Grid"), # Make on_click explicit
            icon_button("ruler", on_click=CanvasState.toggle_rulers, tooltip="Toggle Rulers"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Edit Tools
        rx.hstack(
            icon_button("copy", CanvasState.duplicate_selected_nodes, "Duplicate Selected"),
            icon_button("trash-2", CanvasState.delete_selected_nodes, "Delete Selected"),
            icon_button("folder-plus", CanvasState.group_selected_nodes, "Group Selected"),
            spacing="1",
            class_name="bg-gray-800 rounded-lg p-2 border border-gray-700"
        ),

        # Canvas Actions
        rx.hstack(
            primary_button("Generate", CanvasState.generate_visual, "sparkles", variant="success"),
            primary_button("Clear All", CanvasState.clear_canvas, "trash", variant="danger"), # Clearer label
            primary_button("Export", lambda: setattr(CanvasState, "show_export_modal", True), "download"), # Ensure show_export_modal is a Var or setattr works
            spacing="2"
        ),
        spacing="3",
        width="100%",
        padding="0.75rem",
        class_name="bg-gray-900 shadow-lg border-b border-gray-700 flex-wrap justify-start md:justify-between gap-3", # Added gap
        align_items="center"
    )

def enhanced_canvas():
    return rx.box(
        react_flow(
            nodes=CanvasState.nodes, # Bind to state
            edges=CanvasState.edges, # Bind to state
            on_nodes_change=CanvasState.on_nodes_change, # Event handler
            on_edges_change=lambda changes: setattr(CanvasState, 'edges', CanvasState.edges), # Basic handler if edges are directly manipulated by RF
            on_connect=CanvasState.on_connect,
            on_pane_click=CanvasState.deselect_node, # Deselects internal selected_node
            on_node_click=lambda event, node: CanvasState.select_node(node["id"]), # Select node on click
            fit_view=True,
            nodes_draggable=True,
            nodes_connectable=True,
            elements_selectable=True,
            min_zoom=0.2,
            max_zoom=4.0,
            # default_zoom=CanvasState.zoom_level, # Control zoom via state Var if needed elsewhere
            # style prop for ReactFlow itself is usually for dimensions, not complex backgrounds
            class_name="w-full flex-1 border border-[var(--gray-a5)] rounded-lg relative bg-[var(--gray-a2)]" # Use Radix vars
        ),
        # Children like Background, Controls, MiniMap should be direct children of react_flow
        # According to reactflow.py structure, they are passed as children components.
        # The example from reactflow.py needs to be adapted if it implies they are props.
        # Assuming they are children:
        background(variant=rx.cond(CanvasState.grid_enabled, "dots", "lines"), gap=20, size=1),
        controls(), # show_interactive=True, show_fit_view=True, show_zoom=True are defaults
        mini_map(pannable=True, zoomable=True),


        # Rulers (conditional) - simplified for overlay
        rx.cond(
            CanvasState.rulers_enabled,
            rx.fragment(
                rx.box(class_name="absolute top-0 left-8 right-0 h-8 bg-[var(--gray-a3)] border-b border-[var(--gray-a5)] z-[1] pointer-events-none"),
                rx.box(class_name="absolute left-0 top-8 bottom-0 w-8 bg-[var(--gray-a3)] border-r border-[var(--gray-a5)] z-[1] pointer-events-none"),
            )
        ),

        # Selection info
        rx.cond(
            rx.length(CanvasState.selected_nodes) > 0, # Use rx.length for UI display of list length
            rx.box(
                rx.text(
                    rx.text.concat(rx.length(CanvasState.selected_nodes).to_string(), " node(s) selected"),
                    color_scheme="gray", high_contrast=True, size="1" # Radix text props
                ),
                class_name="absolute bottom-3 left-3 bg-[var(--gray-a3)] px-2 py-1 rounded border border-[var(--gray-a5)] shadow-md z-[2]"
            )
        ),

        # Zoom indicator
        rx.box(
            rx.text(
                rx.text.concat((CanvasState.zoom_level * 100).round().to_string(), "%"), # Display zoom from state
                 color_scheme="gray", high_contrast=True, size="1"
            ),
            class_name="absolute bottom-3 right-3 bg-[var(--gray-a3)] px-2 py-1 rounded border border-[var(--gray-a5)] shadow-md z-[2]"
        ),
        class_name="relative flex-1", # This box is the container for ReactFlow and overlays
        # Height calculation depends on toolbar height. If toolbar is ~60px:
        style={"height": "calc(100vh - 70px)"} # Adjusted height calculation
    )


def properties_panel_content(node: rx.Var[Dict[str, Any]]): # Pass node as a Var
    # This function will be called by rx.cond, so node will be the selected_node
    # We need to ensure that we access its fields as Vars if they are meant to be editable.
    # For simplicity, we'll display them. Editing would require binding to specific State methods.

    # Placeholder for a function that would update node data in CanvasState
    def update_node_data(field: str, value: Any):
        # This is tricky because `node` here is a copy or a Var proxy.
        # The actual update must happen on `CanvasState.nodes` list.
        # CanvasState.update_selected_node_data(field, value) # Needs implementation
        print(f"Placeholder: Update {node.get('id', '')} field '{field}' to '{value}'")
        # Example of how it might look in CanvasState:
        # for i, n_state in enumerate(self.nodes):
        #     if n_state["id"] == self.selected_node["id"]:
        #         self.nodes[i]["data"][field] = value
        #         self.selected_node = self.nodes[i] # Refresh selected_node
        #         break


    return rx.vstack(
        card([
            rx.text(rx.text.concat("Node: ", node.get("data", {}).get("label", "N/A")), weight="bold"),
            rx.text(rx.text.concat("ID: ", node.get("id", "N/A")), size="1", color_scheme="gray"),
            rx.text(rx.text.concat("Type: ", node.get("type", "N/A")), size="1", color_scheme="gray"),
        ], title="Node Information"),

        card([
            rx.hstack(
                rx.vstack(
                    rx.text("X", size="1", color_scheme="gray"),
                    # For direct editing, this input would need to call an event handler
                    # that updates CanvasState.nodes[...]["position"]["x"]
                    rx.input(
                        value=node.get("position", {}).get("x", 0).to_string(),
                        # on_change=lambda val: update_node_data("position_x", val) # Needs full implementation
                        type="number", placeholder="X", size="1"
                    ),
                ),
                rx.vstack(
                    rx.text("Y", size="1", color_scheme="gray"),
                    rx.input(
                        value=node.get("position", {}).get("y", 0).to_string(),
                        # on_change=lambda val: update_node_data("position_y", val)
                        type="number", placeholder="Y", size="1"
                    ),
                ),
                spacing="3",
            )
        ], title="Position"),

        # Example for a specific node type (e.g., if it's an AI processor)
        rx.cond(
            node.get("data", {}).get("label", "").contains("AI Generator"),
            card([
                rx.text("Prompt", size="1", color_scheme="gray"),
                rx.text_area(
                    value=node.get("data", {}).get("prompt", ""),
                    # on_change=lambda val: update_node_data("prompt", val),
                    placeholder="Enter AI prompt...",
                    rows=3,
                    size="1"
                ),
            ], title="AI Prompt")
        ),
        spacing="4",
        width="100%"
    )

def properties_panel():
    return sidebar_panel(
        "Properties",
        [
            rx.cond(
                CanvasState.selected_node.contains("id"), # Check if a node is selected
                properties_panel_content(CanvasState.selected_node), # Pass the selected node
                rx.center( # If no node selected
                    rx.text("Select a node to see its properties.", color_scheme="gray", align="center"),
                    height="100%",
                )
            )
        ],
        is_open=CanvasState.show_properties_panel # Assumes this is a Var[bool] in CanvasState
    )


def layers_panel():
    return sidebar_panel(
        "Layers",
        [
            rx.cond(
                rx.length(CanvasState.nodes) > 0,
                rx.vstack(
                    rx.foreach(
                        CanvasState.nodes, # Iterate over nodes
                        lambda node: rx.hstack(
                            rx.icon(tag="square", size=14, margin_right="0.5em",
                                    color_scheme=rx.cond(CanvasState.selected_node.get("id") == node.get("id"), "accent", "gray")),
                            rx.text(
                                node.get("data", {}).get("label", node.get("id")),
                                size="2",
                                weight=rx.cond(CanvasState.selected_node.get("id") == node.get("id"), "bold", "regular"),
                                color_scheme=rx.cond(CanvasState.selected_node.get("id") == node.get("id"), "accent", "gray"),
                                flex_grow=1,
                                truncate=True,
                            ),
                            # Add visibility/lock icons later, need state per node
                            # icon_button("eye", size="sm", variant="ghost"),
                            # icon_button("lock", size="sm", variant="ghost"),
                            spacing="2",
                            align="center",
                            width="100%",
                            padding="0.3rem 0.5rem",
                            border_radius="var(--radius-2)",
                            _hover={"background_color": "var(--gray-a3)"},
                            background_color=rx.cond(CanvasState.selected_node.get("id") == node.get("id"), "var(--accent-3)", "transparent"),
                            cursor="pointer",
                            on_click=lambda: CanvasState.select_node(node.get("id"))
                        )
                    ),
                    spacing="1",
                    width="100%",
                    max_height="40vh", # Limit height and allow scroll
                    overflow_y="auto"
                ),
                rx.center(
                    rx.text("No nodes on canvas.", color_scheme="gray"),
                    height="100%"
                )
            )
        ],
        is_open=CanvasState.show_layers_panel # Assumes this is a Var[bool] in CanvasState
    )


def ai_assistant_panel():
    # This needs to be a Var to be reactive in the UI if suggestions change
    _current_suggestions_var = rx.Var.create(CanvasState.generate_prompt_suggestions())

    return card([
        rx.vstack(
            rx.heading("AI Assistant", size="5"), # Radix size

            # Model Selection
            rx.text("AI Model", size="1", color_scheme="gray", margin_bottom="0.25rem"),
            rx.select.root(
                rx.select.trigger(placeholder="Select AI Model", width="100%", size="2"),
                rx.select.content(
                    rx.foreach(
                        CanvasState.available_models,
                        lambda model: rx.select.item(model.get("name"), value=model.get("id"))
                    )
                ),
                value=CanvasState.selected_model, # Bind to state
                on_change=lambda val: setattr(CanvasState, "selected_model", val),
                width="100%"
            ),

            # Prompt Suggestions
            rx.hstack(
                rx.text("Prompt Suggestions", size="1", color_scheme="gray", margin_top="1rem"),
                icon_button(
                    "refresh-cw",
                    on_click=lambda: _current_suggestions_var.set(CanvasState.generate_prompt_suggestions()),
                    size="sm", class_name="ml-auto", variant="ghost" # Radix variant
                ),
                width="100%", justify="space-between", align_items="center"
            ),
            rx.vstack(
                rx.foreach(
                    _current_suggestions_var, # Use the Var here
                    lambda suggestion: rx.button(
                        suggestion,
                        variant="outline", color_scheme="gray", width="100%",
                        text_align="left", size="1", class_name="truncate",
                        on_click=lambda: print(f"Suggestion: {suggestion}") # Placeholder action
                    )
                ),
                spacing="1", width="100%", margin_top="0.25rem"
            ),

            # Generation Settings - Steps
            rx.text("Steps", size="1", color_scheme="gray", margin_top="1rem"),
            rx.hstack(
                rx.slider(
                    value=[CanvasState.model_settings.get("steps", 50)], # Slider value is a list
                    min=10, max=150, step=1,
                    on_value_commit=lambda val_list: CanvasState.update_model_settings("steps", val_list[0]),
                    flex_grow=1
                ),
                rx.text(CanvasState.model_settings.get("steps", 50).to_string(), size="2", min_width="3em", text_align="right"),
                spacing="3", width="100%", align_items="center"
            ),

            primary_button("Generate Image", CanvasState.generate_visual, "sparkles", variant="success", class_name="w-full mt-4"),
            spacing="4"
        )
    ], class_name="w-80 h-full overflow-y-auto p-4") # Ensure it can scroll if content overflows
