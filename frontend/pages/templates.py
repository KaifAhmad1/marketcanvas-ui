import reflex as rx
from ..components.ui_components import primary_button, card, icon_button
from ..state.canvas_state import CanvasState

def templates():
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Templates", size="2xl", color="white"),
            primary_button("Back to Editor", lambda: rx.redirect("/editor"), "arrow-left"),
            justify="space-between",
            width="100%",
            padding="2rem"
        ),
        
        # Template Categories
        rx.hstack(
            primary_button("All", variant="outline"),
            primary_button("Social Media", variant="outline"),
            primary_button("Advertising", variant="outline"),
            primary_button("Branding", variant="outline"),
            primary_button("Print", variant="outline"),
            spacing="4",
            padding_x="2rem"
        ),
        
        # Templates Grid
        rx.box(
            rx.grid(
                rx.foreach(
                    CanvasState.templates,
                    lambda template, index: card([
                        rx.image(
                            src=template.get("preview", "/api/placeholder/300/200"),
                            class_name="w-full h-48 object-cover rounded-lg mb-4"
                        ),
                        rx.text(template.get("name", "Template"), 
                               color="white", font_weight="bold", font_size="lg"),
                        rx.text(template.get("category", "General"), 
                               color="gray.400", font_size="sm"),
                        rx.hstack(
                            primary_button(
                                "Use Template", 
                                lambda t=template: [
                                    CanvasState.load_template(t.get("id", "")),
                                    rx.redirect("/editor")
                                ],
                                "plus"
                            ),
                            icon_button("eye", tooltip="Preview"),
                            spacing="2",
                            class_name="mt-4"
                        )
                    ])
                ),
                columns="repeat(auto-fill, minmax(300px, 1fr))",
                gap="6",
                width="100%"
            ),
            class_name="flex-1 px-8 pb-8"
        ),
        
        class_name="min-h-screen bg-gray-900",
        spacing="0"
    )
