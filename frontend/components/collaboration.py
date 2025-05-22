import reflex as rx
from ..state.canvas_state import CanvasState
from .ui_components import primary_button

def collaboration_panel():
    return rx.box(
        rx.vstack(
            rx.text("Collaborators", font_weight="bold", font_size="1.2em", class_name="text-gray-200"),
            rx.foreach(
                CanvasState.collaborators,
                lambda user: rx.hstack(
                    rx.text(user["name"], class_name="text-gray-200"),
                    rx.box(
                        class_name=f"w-3 h-3 rounded-full {'bg-green-500' if user['active'] else 'bg-red-500'}",
                    ),
                    spacing="2",
                ),
            ),
            primary_button("Invite User", CanvasState.invite_collaborator, icon="user-plus"),
            spacing="2",
            padding="1rem",
            class_name="w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-lg glass",
        ),
        class_name="absolute left-4 top-20",
        role="region",
        aria_label="Collaboration panel",
    )
