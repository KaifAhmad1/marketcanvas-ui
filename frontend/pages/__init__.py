# frontend/pages/__init__.py
import reflex as rx
from .editor import editor
from .welcome import welcome

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        radius="large",
        scaling="100%"
    )
)

app.add_page(welcome, route="/", title="MarketCanvas AI - Welcome")
app.add_page(editor, route="/editor", title="MarketCanvas AI - Editor")
