import reflex as rx
from ..state.canvas_state import CanvasState

def apply_theme():
    return rx.fragment(
        rx.cond(
            CanvasState.theme == "dark",
            rx.html(f"""
                <style>
                    :root {{
                        --background: {CanvasState.theme_background};
                        --text: #f3f4f6;
                        --accent: {CanvasState.accent_color};
                        --canvas-bg: linear-gradient(135deg, #1f2937, #374151);
                        --font-family: {CanvasState.theme_font};
                    }}
                </style>
            """),
            rx.html(f"""
                <style>
                    :root {{
                        --background: #f9fafb;
                        --text: #111827;
                        --accent: {CanvasState.accent_color};
                        --canvas-bg: linear-gradient(135deg, #f9fafb, #e5e7eb);
                        --font-family: {CanvasState.theme_font};
                    }}
                </style>
            """),
        ),
    )
