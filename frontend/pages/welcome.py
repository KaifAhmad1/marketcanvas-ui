# frontend/pages/welcome.py
import reflex as rx
from ..components.ui_components import primary_button, card
from ..state.canvas_state import CanvasState # Make sure CanvasState is imported

def welcome():
    return rx.vstack(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "AI Visual Generator",
                    color="white",
                    text_align="center",
                    class_name="text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
                ),
                rx.text(
                    "Create stunning visuals with AI-powered node-based workflows",
                    color="gray.300",
                    text_align="center",
                    class_name="max-w-2xl text-lg md:text-xl"
                ),
                rx.hstack(
                    primary_button("Start Creating", lambda: rx.redirect("/editor"), "plus", variant="primary"),
                    primary_button("View Templates", lambda: rx.redirect("/templates"), "layout-template", variant="outline"),
                    primary_button("Tutorial", CanvasState.start_tutorial, "play", variant="secondary"),
                    spacing="4",
                    class_name="mt-6"
                ),
                spacing="6",
                align="center"
            ),
            class_name="flex items-center justify-center min-h-[60vh] text-center px-4"
        ),

        # Features Section
        # ... (rest of the features section is fine) ...
        rx.box(
            rx.vstack(
                rx.heading("Features", class_name="text-3xl md:text-4xl font-bold text-white text-center"),
                rx.grid(
                    card([
                        rx.icon(tag="cpu", size=32, color_scheme="blue"),
                        rx.heading("AI-Powered Generation", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Multiple AI models including DALL-E 3, Midjourney, and Stable Diffusion",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    card([
                        rx.icon(tag="workflow", size=32, color_scheme="purple"),
                        rx.heading("Node-Based Workflow", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Visual programming interface for complex image generation pipelines",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    card([
                        rx.icon(tag="git-fork", size=32, color_scheme="green"),
                        rx.heading("A/B Testing", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Compare different variations and optimize your visual content",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    card([
                        rx.icon(tag="users", size=32, color_scheme="orange"),
                        rx.heading("Collaboration", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Work together with your team in real-time",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    card([
                        rx.icon(tag="layout-template", size=32, color_scheme="pink"),
                        rx.heading("Templates", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Pre-built workflows for common use cases",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    card([
                        rx.icon(tag="download", size=32, color_scheme="cyan"),
                        rx.heading("Export Options", class_name="text-xl font-semibold text-white mt-2"),
                        rx.text("Multiple formats and sizes for any platform",
                               color_scheme="gray", class_name="text-sm mt-1")
                    ]),
                    columns="1 md:2 lg:3",
                    gap="6",
                    width="100%"
                ),
                spacing="8"
            ),
            class_name="py-16 px-8"
        ),

        # Recent Projects (if any)
        rx.cond(
            CanvasState.has_saved_projects,
            rx.box(
                rx.vstack(
                    rx.heading("Recent Projects", class_name="text-3xl md:text-4xl font-bold text-white"),
                    rx.grid(
                        rx.foreach(
                            CanvasState.saved_projects[:6],
                            lambda project, index: card([
                                rx.image(
                                    src=project.get("preview_image", "/placeholder/200/150.svg"),
                                    class_name="w-full h-32 object-cover rounded mb-3"
                                ),
                                rx.text(project.get("name", "Untitled"),
                                       class_name="text-white font-bold"),
                                # CORRECTED: Use rx.let to resolve the Var to a Python string for slicing
                                rx.let(
                                    # Bind the Var project.get('updated_at', '') to python_date_str
                                    python_date_str=project.get('updated_at', '') 
                                )( 
                                    # Inside this lambda, python_date_str is a Python string
                                    lambda python_date_str_resolved: rx.text( 
                                        f"Updated {python_date_str_resolved[:10]}",
                                        color_scheme="gray", class_name="text-xs mt-1"
                                    )
                                ),
                                primary_button(
                                    "Open",
                                    lambda p=project: [
                                        CanvasState.load_project(p.get("id")),
                                        rx.redirect("/editor")
                                    ],
                                    "folder-open",
                                    variant="outline"
                                )
                            ])
                        ),
                        columns="1 sm:2 md:3",
                        gap="4",
                        width="100%"
                    ),
                    spacing="6",
                    align="start"
                ),
                class_name="py-16 px-8"
            ),
            rx.box()
        ),

        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
