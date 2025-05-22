# frontend/components/reactflow.py
import reflex as rx

class ReactFlow(rx.Component):
    library = "reactflow"
    tag = "ReactFlow"
    nodes: rx.Var[list] = []
    edges: rx.Var[list] = []
    on_nodes_change: rx.EventHandler[lambda e0: [e0]]
    on_edges_change: rx.EventHandler[lambda e0: [e0]]
    on_connect: rx.EventHandler[lambda e0: [e0]]
    on_pane_click: rx.EventHandler[lambda e0: [e0]]
    on_node_click: rx.EventHandler[lambda e0, e1: [e0, e1]]
    fit_view: rx.Var[bool] = True
    nodes_draggable: rx.Var[bool] = True
    nodes_connectable: rx.Var[bool] = True
    elements_selectable: rx.Var[bool] = True
    min_zoom: rx.Var[float] = 0.2
    max_zoom: rx.Var[float] = 4.0

react_flow = ReactFlow.create

class Background(rx.Component):
    library = "reactflow"
    tag = "Background"
    variant: rx.Var[str] = "dots"
    gap: rx.Var[int] = 20
    size: rx.Var[float] = 1
    color: rx.Var[str] = "#aaa"

background = Background.create

class Controls(rx.Component):
    library = "reactflow"
    tag = "Controls"

controls = Controls.create

class MiniMap(rx.Component):
    library = "reactflow"
    tag = "MiniMap"
    pannable: rx.Var[bool] = True
    zoomable: rx.Var[bool] = True

mini_map = MiniMap.create
