import reflex as rx
from ..components.ui_components import primary_button, card
from ..state.canvas_state import CanvasState

def welcome():
    return rx.vstack(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "AI Visual Generator",
                    size="4xl",
                    color="white",
                    text_align="center",
                    class_name="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
                ),
                rx.text(
                    "Create stunning visuals with AI-powered node-based workflows",
                    size="xl",
                    color="gray.300",
                    text_align="center",
                    class_name="max-w-2xl"
                ),
                rx.hstack(
                    primary_button("Start Creating", lambda: rx.redirect("/editor"), "plus", variant="primary"),
                    primary_button("View Templates", lambda: rx.redirect("/templates"), "template", variant="outline"),
                    primary_button("Tutorial", CanvasState.start_tutorial, "play-circle", variant="secondary"),
                    spacing="4"
                ),
                spacing="6",
                align="center"
            ),
            class_name="flex items-center justify-center min-h-[60vh] text-center"
        ),
        
        # Features Section
        rx.box(
            rx.vstack(
                rx.heading("Features", size="2xl", color="white", text_align="center"),
                rx.grid(
                    card([
                        rx.icon(tag="cpu", size=32, color="blue.500"),
                        rx.heading("AI-Powered Generation", size="lg", color="white"),
                        rx.text("Multiple AI models including DALL-E 3, Midjourney, and Stable Diffusion", 
                               color="gray.400")
                    ]),
                    card([
                        rx.icon(tag="workflow", size=32, color="purple.500"),
                        rx.heading("Node-Based Workflow", size="lg", color="white"),
                        rx.text("Visual programming interface for complex image generation pipelines", 
                               color="gray.400")
                    ]),
                    card([
                        rx.icon(tag="split", size=32, color="green.500"),
                        rx.heading("A/B Testing", size="lg", color="white"),
                        rx.text("Compare different variations and optimize your visual content", 
                               color="gray.400")
                    ]),
                    card([
                        rx.icon(tag="users", size=32, color="orange.500"),
                        rx.heading("Collaboration", size="lg", color="white"),
                        rx.text("Work together with your team in real-time", 
                               color="gray.400")
                    ]),
                    card([
                        rx.icon(tag="template", size=32, color="pink.500"),
                        rx.heading("Templates", size="lg", color="white"),
                        rx.text("Pre-built workflows for common use cases", 
                               color="gray.400")
                    ]),
                    card([
                        rx.icon(tag="download", size=32, color="cyan.500"),
                        rx.heading("Export Options", size="lg", color="white"),
                        rx.text("Multiple formats and sizes for any platform", 
                               color="gray.400")
                    ]),
                    columns="repeat(auto-fit, minmax(300px, 1fr))",
                    gap="6",
                    width="100%"
                ),
                spacing="8"
            ),
            class_name="py-16 px-8"
        ),
        
        # Recent Projects (if any)
        rx.cond(
            CanvasState.saved_projects,
            rx.box(
                rx.vstack(
                    rx.heading("Recent Projects", size="2xl", color="white"),
                    rx.grid(
                        rx.foreach(
                            CanvasState.saved_projects[:6],  # Show last 6 projects
                            lambda project, index: card([
                                rx.image(
                                    src=project.get("preview_image", "/api/placeholder/200/150"),
                                    class_name="w-full h-32 object-cover rounded mb-3"
                                ),
                                rx.text(project.get("name", "Untitled"), 
                                       color="white", font_weight="bold"),
                                rx.text(f"Updated {project.get('updated_at', '')[:10]}", 
                                       color="gray.400", font_size="sm"),
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
                        columns="repeat(auto-fit, minmax(250px, 1fr))",
                        gap="4",
                        width="100%"
                    ),
                    spacing="6"
                ),
                class_name="py-16 px-8"
            ),
            rx.box()
        ),
        
        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
