import reflex as rx
from typing import Any, Dict, List, Union, Optional, Callable

class ReactFlowLib(rx.Component):
    library = "reactflow" # Tells Reflex to import 'reactflow' JS library
    def _get_custom_code(self) -> str:
        return "import 'reactflow/dist/style.css';" # Import necessary CSS

class ReactFlow(ReactFlowLib):
    tag = "ReactFlow" # Corresponds to <ReactFlow /> in JS

    # Core Props
    nodes: rx.Var[List[Dict[str, Any]]]
    edges: rx.Var[List[Dict[str, Any]]]

    # Behavior Props
    fit_view: rx.Var[bool] = True
    nodes_draggable: rx.Var[bool] = True
    edges_updatable: rx.Var[bool] = True # Allow dragging edge ends to new targets/sources
    nodes_connectable: rx.Var[bool] = True
    nodes_focusable: rx.Var[bool] = True # Allow focusing nodes with keyboard
    elevate_nodes_on_drag: rx.Var[bool] = True
    pan_on_drag: rx.Var[Union[bool, List[int]]] = True # Allow panning while dragging node close to edge

    # Style & Viewport Props
    style: rx.Var[Dict[str, Any]] # For custom styling like height, width, border
    default_viewport: rx.Var[Dict[str, Any]] # e.g., {"x": 0, "y": 0, "zoom": 1}
    min_zoom: rx.Var[float] = 0.1
    max_zoom: rx.Var[float] = 4.0

    # Customization Props (Advanced)
    node_types: rx.Var[Dict[str, Any]] # For custom React node components
    edge_types: rx.Var[Dict[str, Any]] # For custom React edge components
    connection_line_style: rx.Var[Dict[str, Any]]
    snap_to_grid: rx.Var[bool] = False
    snap_grid: rx.Var[List[int]] = [15, 15] # [x, y] grid size

    # Event Handlers (lambda e0: [e0] passes the first argument from JS event)
    on_nodes_change: rx.EventHandler[lambda changes: [changes]]
    on_edges_change: rx.EventHandler[lambda changes: [changes]]
    on_connect: rx.EventHandler[lambda connection_params: [connection_params]]
    on_node_click: rx.EventHandler[lambda event, node_data: [node_data]] # Pass JS event and node object
    on_pane_click: rx.EventHandler[lambda event: []] # Pass JS event
    on_node_drag_stop: rx.EventHandler[lambda event, node_data, nodes: [node_data]] # node_data for dragged node
    on_init: rx.EventHandler[lambda react_flow_instance: []] # Called with ReactFlow instance
    # Add more event handlers as needed: onMoveEnd, onSelectionChange, etc.

class Background(ReactFlowLib):
    tag = "Background"
    variant: rx.Var[str] = "dots" # 'dots', 'lines', 'cross'
    gap: rx.Var[Union[int, List[int]]] = 16
    size: rx.Var[int] = 1
    color: rx.Var[str] # Will be set by CSS variables for theming
    style: rx.Var[Dict[str, Any]] # For additional styling if needed

class Controls(ReactFlowLib):
    tag = "Controls"
    show_fit_view: rx.Var[bool] = True
    show_interactive: rx.Var[bool] = True # Toggle node interactivity
    show_zoom: rx.Var[bool] = True
    position: rx.Var[str] = "bottom-right" # 'top-left', 'top-right', 'bottom-left', 'bottom-right'
    style: rx.Var[Dict[str, Any]]

class MiniMap(ReactFlowLib):
    tag = "MiniMap"
    # Node color can be a function: (node) => node.style?.background || '#eee'
    node_color: rx.Var[Union[str, Callable[[Dict], str]]]
    node_stroke_color: rx.Var[Union[str, Callable[[Dict], str]]] # For borders of nodes in minimap
    node_border_radius: rx.Var[int] = 2
    mask_color: rx.Var[str] = "rgba(200, 200, 200, 0.6)" # The overlay color
    pannable: rx.Var[bool] = True
    zoomable: rx.Var[bool] = True
    style: rx.Var[Dict[str, Any]]

# Create-able instances for easier use
react_flow = ReactFlow.create
background = Background.create
controls = Controls.create
minimap = MiniMap.create
