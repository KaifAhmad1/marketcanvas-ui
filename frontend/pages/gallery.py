# frontend/pages/gallery.py
import reflex as rx
from ..components.ui_components import primary_button, card, icon_button # Added icon_button
from ..state.canvas_state import CanvasState

def gallery():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Generated Gallery", class_name="text-3xl md:text-4xl font-bold text-white"), # Corrected size
            primary_button("Back to Editor", lambda: rx.redirect("/editor"), "arrow-left"),
            justify="space-between",
            width="100%",
            padding="2rem"
        ),

        # Gallery Grid
        rx.box(
            rx.cond(
                CanvasState.generation_history, # This might need to be len(CanvasState.generation_history) > 0
                rx.grid(
                    rx.foreach(
                        CanvasState.generation_history,
                        lambda item, index: card([
                            rx.image(
                                src=item.get("image_url", "/api/placeholder/300/300"),
                                class_name="w-full h-48 object-cover rounded-lg mb-4"
                            ),
                            rx.text(f"Generated {item.get('timestamp', '')[:10]}",
                                   color_scheme="gray", class_name="text-sm"),
                            rx.text(f"Model: {item.get('model', 'Unknown')}",
                                   color_scheme="gray", class_name="text-sm"),
                            rx.text(f"Nodes: {item.get('nodes_used', 0)}",
                                   color_scheme="gray", class_name="text-sm"),
                            rx.hstack(
                                icon_button("download", tooltip="Download"),
                                icon_button("share-2", tooltip="Share"), # 'share-2' is more common for lucide
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
                        rx.icon(tag="image-off", size=64, color_scheme="gray"), # image-off or similar for empty
                        rx.text("No images generated yet", color_scheme="gray", class_name="text-lg mt-2"),
                        rx.text("Create your first visual in the editor", color_scheme="gray", class_name="text-sm"),
                        primary_button("Start Creating", lambda: rx.redirect("/editor"), "plus", class_name="mt-4"),
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
