import reflex as rx
from ..components.ui_components import primary_button, card, tabs
from ..state.canvas_state import CanvasState

def settings():
    general_settings = rx.vstack(
        card([
            rx.heading("Theme", size="md", color="white"),
            rx.hstack(
                rx.button(
                    "Dark",
                    class_name="bg-gray-700 text-white px-4 py-2 rounded",
                    on_click=lambda: CanvasState.set_theme("dark")
                ),
                rx.button(
                    "Light", 
                    class_name="bg-gray-200 text-gray-800 px-4 py-2 rounded",
                    on_click=lambda: CanvasState.set_theme("light")
                ),
                spacing="2"
            ),
            rx.text("Accent Color", color="gray.400", font_size="sm", class_name="mt-4"),
            rx.hstack(
                *[
                    rx.box(
                        class_name=f"w-8 h-8 rounded cursor-pointer border-2 border-gray-600",
                        style={"background": color},
                        on_click=lambda c=color: CanvasState.set_accent_color(c)
                    )
                    for color in ["#3b82f6", "#8b5cf6", "#ef4444", "#f59e0b", "#10b981", "#f97316"]
                ],
                spacing="2"
            )
        ]),
        
        card([
            rx.heading("Canvas", size="md", color="white"),
            rx.vstack(
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.auto_save_enabled,
                        on_change=CanvasState.toggle_auto_save
                    ),
                    rx.text("Auto-save enabled", color="white"),
                    spacing="2"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.grid_enabled,
                        on_change=CanvasState.toggle_grid
                    ),
                    rx.text("Show grid", color="white"),
                    spacing="2"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.snap_to_grid,
                        on_change=CanvasState.toggle_snap_to_grid
                    ),
                    rx.text("Snap to grid", color="white"),
                    spacing="2"
                ),
                spacing="3"
            )
        ]),
        
        spacing="6"
    )
    
    ai_settings = rx.vstack(
        card([
            rx.heading("AI Models", size="md", color="white"),
            rx.vstack(
                rx.foreach(
                    CanvasState.available_models,
                    lambda model, index: rx.hstack(
                        rx.radio(
                            value=model["id"],
                            checked=model["id"] == CanvasState.selected_model
                        ),
                        rx.vstack(
                            rx.text(model["name"], color="white", font_weight="bold"),
                            rx.text(f"{model['provider']} • {model['speed']} • {model['quality']}", 
                                   color="gray.400", font_size="sm"),
                            spacing="1",
                            align="start"
                        ),
                        spacing="3",
                        align="center",
                        width="100%",
                        class_name="p-3 border border-gray-700 rounded hover:bg-gray-800 cursor-pointer"
                    )
                ),
                spacing="2"
            )
        ]),
        
        card([
            rx.heading("Generation Settings", size="md", color="white"),
            rx.vstack(
                rx.hstack(
                    rx.text("Render Quality:", color="gray.400"),
                    rx.select(
                        ["Low", "Medium", "High", "Ultra"],
                        value=CanvasState.render_quality,
                        on_change=CanvasState.set_render_quality
                    ),
                    justify="space-between"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.real_time_preview,
                        on_change=CanvasState.toggle_real_time_preview
                    ),
                    rx.text("Real-time preview", color="white"),
                    spacing="2"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.gpu_acceleration,
                        on_change=lambda: setattr(CanvasState, "gpu_acceleration", not CanvasState.gpu_acceleration)
                    ),
                    rx.text("GPU acceleration", color="white"),
                    spacing="2"
                ),
                spacing="3"
            )
        ]),
        
        spacing="6"
    )
    
    performance_settings = rx.vstack(
        card([
            rx.heading("Performance Metrics", size="md", color="white"),
            rx.vstack(
                rx.foreach(
                    CanvasState.get_performance_metrics().items(),
                    lambda item: rx.hstack(
                        rx.text(f"{item[0].replace('_', ' ').title()}:", color="gray.400"),
                        rx.text(str(item[1]), color="white"),
                        justify="space-between"
                    )
                ),
                spacing="2"
            )
        ]),
        
        card([
            rx.heading("Usage Analytics", size="md", color="white"),
            rx.vstack(
                rx.foreach(
                    CanvasState.analytics.items(),
                    lambda item: rx.hstack(
                        rx.text(f"{item[0].replace('_', ' ').title()}:", color="gray.400"),
                        rx.text(str(item[1]), color="white"),
                        justify="space-between"
                    )
                ),
                spacing="2"
            )
        ]),
        
        spacing="6"
    )
    
    tabs_data = [
        {"label": "General", "value": "general", "content": general_settings},
        {"label": "AI Models", "value": "ai", "content": ai_settings},
        {"label": "Performance", "value": "performance", "content": performance_settings}
    ]
    
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Settings", size="2xl", color="white"),
            primary_button("Back to Editor", lambda: rx.redirect("/editor"), "arrow-left"),
            justify="space-between",
            width="100%",
            padding="2rem"
        ),
        
        # Settings Content
        rx.box(
            tabs(tabs_data, "general"),
            class_name="flex-1 px-8 pb-8"
        ),
        
        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
