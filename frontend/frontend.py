import reflex as rx
from .pages.editor import editor
from .pages.welcome import welcome
from .pages.gallery import gallery
from .pages.templates import templates
from .pages.settings import settings

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        panel_background="solid",
    ),
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "/assets/main.css",
    ],
)

app.add_page(welcome, route="/")
app.add_page(editor, route="/editor")
app.add_page(gallery, route="/gallery")
app.add_page(templates, route="/templates")
app.add_page(settings, route="/settings")
