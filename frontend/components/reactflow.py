import reflex as rx

class ReactFlow(rx.Component):
    library = "reactflow"
    tag = "ReactFlow"
    
    # Core props
    nodes: rx.Var[list] = []
    edges: rx.Var[list] = []
    on_nodes_change: rx.EventHandler[lambda changes: changes]
    on_edges_change: rx.EventHandler[lambda changes: changes]
    on_connect: rx.EventHandler[lambda connection: connection]
    
    # Interaction props
    nodes_draggable: rx.Var[bool] = True
    nodes_connectable: rx.Var[bool] = True
    elements_selectable: rx.Var[bool] = True
    
    # Viewport props
    fit_view: rx.Var[bool] = True
    fit_view_options: rx.Var[dict] = {}
    min_zoom: rx.Var[float] = 0.5
    max_zoom: rx.Var[float] = 2.0
    default_viewport: rx.Var[dict] = {"x": 0, "y": 0, "zoom": 1}
    
    # Event handlers
    on_pane_click: rx.EventHandler[lambda event: event]
    on_node_click: rx.EventHandler[lambda event, node: [event, node]]
    on_edge_click: rx.EventHandler[lambda event, edge: [event, edge]]

class Background(rx.Component):
    library = "reactflow"
    tag = "Background"
    
    variant: rx.Var[str] = "dots"  # dots, lines, cross
    gap: rx.Var[int] = 20
    size: rx.Var[int] = 1
    color: rx.Var[str] = "#aaa"

class Controls(rx.Component):
    library = "reactflow"
    tag = "Controls"
    
    show_zoom: rx.Var[bool] = True
    show_fit_view: rx.Var[bool] = True
    show_interactive: rx.Var[bool] = True

class MiniMap(rx.Component):
    library = "reactflow"
    tag = "MiniMap"
    
    node_color: rx.Var[str] = "#fff"
    node_border_radius: rx.Var[int] = 2
    mask_color: rx.Var[str] = "rgb(240, 240, 240, 0.6)"
    zoomable: rx.Var[bool] = False
    pannable: rx.Var[bool] = False

# Factory functions
def react_flow(*children, **props):
    return ReactFlow.create(*children, **props)

def background(**props):
    return Background.create(**props)

def controls(**props):
    return Controls.create(**props)

def mini_map(**props):
    return MiniMap.create(**props)
