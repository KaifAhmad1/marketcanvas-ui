# frontend/pages/settings.py
import reflex as rx
from ..components.ui_components import primary_button, card, tabs
from ..state.canvas_state import CanvasState

def settings():
    general_settings = rx.vstack(
        card([
            rx.heading("Theme", size="5"), # Radix size for medium heading
            rx.hstack(
                rx.button(
                    "Dark",
                    # class_name="bg-gray-700 text-white px-4 py-2 rounded", # Let Radix handle styling
                    on_click=lambda: CanvasState.set_theme("dark"), # Assuming set_theme handles Radix theme change
                    color_scheme="gray", # Example Radix color scheme
                    variant="solid" if CanvasState.theme == "dark" else "soft"
                ),
                rx.button(
                    "Light",
                    on_click=lambda: CanvasState.set_theme("light"),
                    color_scheme="gray",
                    variant="solid" if CanvasState.theme == "light" else "soft"
                ),
                spacing="2"
            ),
            rx.text("Accent Color", color_scheme="gray", class_name="mt-4 text-sm"),
            rx.hstack(
                *[
                    rx.box(
                        class_name=f"w-8 h-8 rounded cursor-pointer border-2",
                        style={
                            "background_color": color,
                            "border_color": rx.cond(CanvasState.accent_color == color, color, "var(--gray-6)")
                        },
                        on_click=lambda c=color: CanvasState.set_accent_color(c)
                    )
                    for color in ["#3b82f6", "#8b5cf6", "#ef4444", "#f59e0b", "#10b981", "#f97316"]
                ],
                spacing="2"
            )
        ], title="Theme Settings"), # Using card title prop

        card([
            # rx.heading("Canvas", size="5"), # Already handled by card title
            rx.vstack(
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.auto_save_enabled,
                        on_change=CanvasState.toggle_auto_save,
                        size="2" # Radix checkbox size
                    ),
                    rx.text("Auto-save enabled", color_scheme="gray"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.grid_enabled,
                        on_change=CanvasState.toggle_grid,
                        size="2"
                    ),
                    rx.text("Show grid", color_scheme="gray"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.snap_to_grid,
                        on_change=CanvasState.toggle_snap_to_grid,
                        size="2"
                    ),
                    rx.text("Snap to grid", color_scheme="gray"),
                    spacing="2",
                    align="center"
                ),
                spacing="3"
            )
        ], title="Canvas Preferences"),

        spacing="6"
    )

    ai_settings = rx.vstack(
        card([
            # rx.heading("AI Models", size="5"),
            rx.vstack(
                rx.radio_group( # Use rx.radio_group for better accessibility
                    rx.foreach(
                        CanvasState.available_models,
                        lambda model, index: rx.label(
                            rx.hstack(
                                rx.radio(
                                    value=model["id"],
                                    # checked=model["id"] == CanvasState.selected_model # Handled by radio_group value
                                ),
                                rx.vstack(
                                    rx.text(model["name"], class_name="font-bold"),
                                    rx.text(f"{model['provider']} • {model['speed']} • {model['quality']}",
                                           color_scheme="gray", class_name="text-xs"), # smaller text
                                    spacing="1",
                                    align="start"
                                ),
                                spacing="3",
                                align="center",
                                width="100%",
                                class_name="p-3 border border-[var(--gray-a6)] rounded hover:bg-[var(--gray-a3)] cursor-pointer"
                            ),
                            width="100%"
                        )
                    ),
                    value=CanvasState.selected_model,
                    on_change=lambda val: setattr(CanvasState, "selected_model", val), # Update state
                    spacing="2",
                    width="100%"
                )
            )
        ], title="AI Models"),

        card([
            # rx.heading("Generation Settings", size="5"),
            rx.vstack(
                rx.hstack(
                    rx.text("Render Quality:", color_scheme="gray"),
                    rx.select(
                        ["Low", "Medium", "High", "Ultra"],
                        value=CanvasState.render_quality,
                        on_change=CanvasState.set_render_quality,
                        size="2" # Radix select size
                    ),
                    justify="space-between",
                    width="100%"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.real_time_preview,
                        on_change=CanvasState.toggle_real_time_preview,
                        size="2"
                    ),
                    rx.text("Real-time preview", color_scheme="gray"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.checkbox(
                        checked=CanvasState.gpu_acceleration,
                        on_change=lambda: setattr(CanvasState, "gpu_acceleration", not CanvasState.gpu_acceleration),
                        size="2"
                    ),
                    rx.text("GPU acceleration", color_scheme="gray"),
                    spacing="2",
                    align="center"
                ),
                spacing="3"
            )
        ], title="Generation Settings"),

        spacing="6"
    )

    performance_settings = rx.vstack(
        card([
            # rx.heading("Performance Metrics", size="5"),
            rx.vstack(
                rx.foreach(
                    CanvasState.get_performance_metrics().items(),
                    lambda item: rx.hstack(
                        rx.text(f"{item[0].replace('_', ' ').title()}:", color_scheme="gray"),
                        rx.text(str(item[1]), class_name="font-semibold"),
                        justify="space-between",
                        width="100%"
                    )
                ),
                spacing="2"
            )
        ], title="Performance Metrics"),

        card([
            # rx.heading("Usage Analytics", size="5"),
            rx.vstack(
                rx.foreach(
                    CanvasState.analytics.items(),
                    lambda item: rx.hstack(
                        rx.text(f"{item[0].replace('_', ' ').title()}:", color_scheme="gray"),
                        rx.text(str(item[1]), class_name="font-semibold"),
                        justify="space-between",
                        width="100%"
                    )
                ),
                spacing="2"
            )
        ], title="Usage Analytics"),

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
            rx.heading("Settings", class_name="text-3xl md:text-4xl font-bold text-white"), # Corrected size
            primary_button("Back to Editor", lambda: rx.redirect("/editor"), "arrow-left"),
            justify="space-between",
            width="100%",
            padding="2rem"
        ),

        # Settings Content
        rx.box(
            tabs(tabs_data, CanvasState.active_settings_tab if hasattr(CanvasState, 'active_settings_tab') else "general", on_tab_change=lambda tab: setattr(CanvasState, 'active_settings_tab', tab)), # Make active tab dynamic
            class_name="flex-1 px-8 pb-8"
        ),

        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
