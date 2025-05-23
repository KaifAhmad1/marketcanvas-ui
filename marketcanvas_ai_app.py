import reflex as rx
from .state.app_state import AppState # Your main state
from .components.react_flow_custom import react_flow, background, controls, minimap
from .components.ui_panels import node_palette_panel, properties_panel, right_sidebar_panel, api_key_input_modal

def editor_page_layout() -> rx.Component:
    """The main editor page layout for MarketCanvas AI."""
    return rx.box( # Root container for global theme class and styles
        rx.hstack(
            # Left Sidebar: Node Palette & Asset Upload
            node_palette_panel(),

            # Center Area: ReactFlow Canvas + Properties Panel on top
            rx.vstack(
                # Top part of center: Properties Panel
                properties_panel(), # This will now be above the canvas conceptually

                # Bottom part of center: ReactFlow Canvas
                rx.box(
                    react_flow(
                        # Children components for ReactFlow
                        background(
                            variant="dots", gap=15, size=1,
                            # Dynamically set background color based on theme for contrast
                            color=rx.cond(AppState.current_ui_theme == "dark", "var(--border-color)", "var(--border-color)")
                        ),
                        controls(position="top-right", style={"background": "var(--panel-bg)", "border": "1px solid var(--border-color)"}),
                        minimap(
                            style={"background": "var(--panel-bg)", "border": "1px solid var(--border-color)"},
                            node_color=lambda n: "var(--primary-accent)" if n.get("selected") else "var(--secondary-accent)",
                            mask_color=rx.color("black", alpha=0.1) # Darker mask for better visibility
                        ),

                        # Core ReactFlow Props
                        nodes=AppState.nodes_for_reactflow,
                        edges=AppState.edges_for_reactflow,
                        on_nodes_change=AppState.on_nodes_change,
                        on_edges_change=AppState.on_edges_change,
                        on_connect=AppState.on_connect,
                        on_node_click=AppState.on_node_click_rf,
                        on_pane_click=AppState.on_pane_click_rf,
                        on_node_drag_stop=AppState.on_node_drag_stop_rf,
                        on_init=AppState.on_react_flow_init, # To get instance for fitView etc.
                        fit_view=True, # Fit view on initial load and when nodes change significantly
                        elevate_nodes_on_drag=True,
                        min_zoom=0.1,
                        max_zoom=3.0,
                        snap_to_grid=True, # Enable snap to grid
                        snap_grid=[10,10], # Grid size
                        connection_line_style={"strokeWidth": 2, "stroke": "var(--primary-accent)"},
                        style={
                            "width": "100%", "height": "100%", # Fill its container
                            "background": "var(--canvas-bg)" # Themeable canvas background
                        },
                    ),
                    flex_grow="1", height="100%", position="relative", # Canvas takes remaining vertical space
                    border_top="1px solid var(--border-color)" # Separator from properties panel
                ),
                spacing="0", # No space between properties panel and canvas
                width="100%", # Full width of the center area
                height="100%",
                flex_grow="1" # Allow center area to grow
            ),

            # Right Sidebar: Tools, Output, Log
            right_sidebar_panel(),

            align_items="stretch", # Make all direct children take full height
            spacing="0", # No space between main layout columns
            width="100%",
            height="100%",
        ),
        api_key_input_modal(), # Add the modal globally, its visibility is controlled by state
        
        # Apply theme class to the root for global CSS variable overrides
        class_name=rx.cond(AppState.current_ui_theme == "dark", "theme-dark", ""),
        width="100vw",
        height="100vh",
        overflow="hidden", # Prevent scrollbars on the body/root
        bg="var(--app-bg)" # Apply themed background to the entire app
    )

# Initialize the Reflex app
app = rx.App(
    state=AppState,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap", # Main UI Font
        "/custom_styles.css", # Your custom global styles (MUST be correctly served by Reflex)
    ],
    head_components=[ # Add meta tags, etc.
        rx.el.title("MarketCanvas AI - Visual Marketing Workflow Editor"),
        rx.el.meta(name="description", content="Create stunning marketing visuals with AI-powered node-based workflows."),
        rx.el.meta(name="viewport", content="width=device-width, initial-scale=1"),
        rx.script("console.log('MarketCanvas AI Frontend Initialized.')") # Example
    ],
    on_load=[AppState.on_app_load] # Call state initialization methods on app load
)
app.add_page(editor_page_layout, route="/", title="MarketCanvas AI Editor") # title here is for browser tab history
