import reflex as rx
from typing import Any, Dict, List, Union

class ReactFlowLib(rx.Component):
    """A component that wraps the ReactFlow library."""
    library = "reactflow@11.10.1"
    
    def _get_custom_code(self) -> str:
        return """
import 'reactflow/dist/style.css';
import '/static/css/canvas.css';
import 'react-color/dist/react-color.min.css';
import 'https://cdn.jsdelivr.net/npm/framer-motion@7.6.1/dist/framer-motion.min.js';
import 'https://cdn.jsdelivr.net/npm/react-hot-toast@2.4.1/dist/react-hot-toast.min.js';
"""

class ReactFlow(ReactFlowLib):
    tag = "ReactFlow"
    
    nodes: rx.Var[List[Dict[str, Any]]]
    edges: rx.Var[List[Dict[str, Any]]]
    fit_view: rx.Var[bool]
    nodes_draggable: rx.Var[bool]
    nodes_connectable: rx.Var[bool]
    nodes_focusable: rx.Var[bool]
    min_zoom: rx.Var[float]
    max_zoom: rx.Var[float]
    default_viewport: rx.Var[Dict[str, float]]
    on_nodes_change: rx.EventHandler[lambda e0: [e0]]
    on_connect: rx.EventHandler[lambda e0: [e0]]
    on_pane_click: rx.EventHandler[lambda e0: [e0]]
    on_node_context_menu: rx.EventHandler[lambda e0: [e0]]
    on_nodes_delete: rx.EventHandler[lambda e0: [e0]]
    on_node_resize: rx.EventHandler[lambda e0: [e0]]
    edge_types: rx.Var[Dict[str, Any]]
    style: rx.Var[Dict[str, Any]]

class Background(ReactFlowLib):
    tag = "Background"
    color: rx.Var[str]
    gap: rx.Var[int]
    size: rx.Var[int]
    variant: rx.Var[str]

class Controls(ReactFlowLib):
    tag = "Controls"
    show_zoom: rx.Var[bool]
    show_fit_view: rx.Var[bool]
    show_interactive: rx.Var[bool]

class MiniMap(ReactFlowLib):
    tag = "MiniMap"
    node_color: rx.Var[str]
    mask_color: rx.Var[str]
    zoomable: rx.Var[bool]
    pannable: rx.Var[bool]

react_flow = ReactFlow.create
background = Background.create
controls = Controls.create
mini_map = MiniMap.create
