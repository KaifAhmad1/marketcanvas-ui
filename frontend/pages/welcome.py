# frontend/pages/welcome.py
import reflex as rx
from ..components.ui_components import primary_button, card
from ..state.canvas_state import CanvasState

def format_date_var_for_display(date_string_var: rx.Var[str]) -> rx.Var[str]:
    return rx.cond(
        date_string_var != "",
        date_string_var.substring(0, 10),
        "N/A"
    )

def welcome():
    return rx.vstack(
        rx.hstack(
            rx.heading("MarketCanvas AI", size="8", class_name="text-white"),
            rx.spacer(),
            primary_button(
                "New Project",
                lambda: rx.redirect("/editor"),
                "plus",
                class_name="mt-4"
            ),
            width="100%",
            padding="1rem",
            align_items="center",
            class_name="bg-gray-900 border-b border-gray-700"
        ),
        rx.vstack(
            rx.heading("Your Projects", size="6", class_name="text-white mb-4"),
            rx.cond(
                CanvasState.has_saved_projects,
                rx.vstack(
                    rx.foreach(
                        CanvasState.saved_projects,
                        lambda project: card([
                            rx.hstack(
                                rx.image(
                                    src=project.get("preview_image", "/placeholder/100/100.svg"),
                                    class_name="w-20 h-20 object-cover rounded"
                                ),
                                rx.vstack(
                                    rx.text(project.get("name", "Untitled"), weight="bold", size="4"),
                                    rx.text(
                                        rx.text.concat("Created: ", format_date_var_for_display(project.get("created_at", ""))),
                                        size="1",
                                        color_scheme="gray"
                                    ),
                                    rx.text(
                                        rx.text.concat("Updated: ", format_date_var_for_display(project.get("updated_at", ""))),
                                        size="1",
                                        color_scheme="gray"
                                    ),
                                    align_items="start",
                                    spacing="1"
                                ),
                                rx.spacer(),
                                primary_button(
                                    "Open",
                                    lambda: CanvasState.load_project(project.get("id")),
                                    "folder-open",
                                    variant="outline",
                                    size="sm"
                                ),
                                spacing="4",
                                width="100%",
                                align_items="center"
                            )
                        ])
                    ),
                    spacing="4",
                    width="100%"
                ),
                rx.text("No projects yet. Create one to get started!", color_scheme="gray")
            ),
            spacing="4",
            padding="2rem",
            width="100%",
            max_width="1200px",
            class_name="mx-auto"
        ),
        spacing="0",
        width="100vw",
        min_height="100vh",
        class_name="bg-[var(--gray-a1)]"
    )
