import reflex as rx
from ..components.ui_components import primary_button, card
from ..state.canvas_state import CanvasState

def gallery():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Generated Gallery", size="2xl", color="white"),
            primary_button("Back to Editor", lambda: rx.redirect("/editor"), "arrow-left"),
            justify="space-between",
            width="100%",
            padding="2rem"
        ),
        
        # Gallery Grid
        rx.box(
            rx.cond(
                CanvasState.generation_history,
                rx.grid(
                    rx.foreach(
                        CanvasState.generation_history,
                        lambda item, index: card([
                            rx.image(
                                src=item.get("image_url", "/api/placeholder/300/300"),
                                class_name="w-full h-48 object-cover rounded-lg mb-4"
                            ),
                            rx.text(f"Generated {item.get('timestamp', '')[:10]}", 
                                   color="gray.400", font_size="sm"),
                            rx.text(f"Model: {item.get('model', 'Unknown')}", 
                                   color="gray.400", font_size="sm"),
                            rx.text(f"Nodes: {item.get('nodes_used', 0)}", 
                                   color="gray.400", font_size="sm"),
                            rx.hstack(
                                icon_button("download", tooltip="Download"),
                                icon_button("share", tooltip="Share"),
                                icon_button("copy", tooltip="Copy"),
                                spacing="2",
                                class_name="mt-4"
                            )
                        ])
                    ),
                    columns="repeat(auto-fill, minmax(300px, 1fr))",
                    gap="6",
                    width="100%"
                ),
                
                # Empty State
                rx.box(
                    rx.vstack(
                        rx.icon(tag="image", size=64, color="gray.500"),
                        rx.text("No images generated yet", color="gray.400", font_size="lg"),
                        rx.text("Create your first visual in the editor", color="gray.500"),
                        primary_button("Start Creating", lambda: rx.redirect("/editor"), "plus"),
                        spacing="4",
                        align="center"
                    ),
                    class_name="flex items-center justify-center h-96"
                )
            ),
            class_name="flex-1 px-8 pb-8"
        ),
        
        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
