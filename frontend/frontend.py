import reflex as rx
from .pages.editor import editor
from .pages.welcome import welcome
from .styles.themes import apply_theme

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        panel_background="solid",
    ),
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
        "https://cdn.jsdelivr.net/npm/react-color@2.19.3/dist/react-color.min.css",
        "https://cdn.jsdelivr.net/npm/react-hot-toast@2.4.1/dist/react-hot-toast.min.css",
        "/static/css/main.css",
    ],
)

app.add_page(welcome, route="/")
app.add_page(editor, route="/editor")
app.add_custom_component(apply_theme)
