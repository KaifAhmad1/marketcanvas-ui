import reflex as rx
from ..components.ui_components import primary_button

def welcome():
    return rx.vstack(
        rx.image(src="/static/assets/logo-dark.png", width="200px", class_name="motion-reduce:animate-bounce"),
        rx.text("Welcome to MarketCanvas AI", font_size="2em", font_weight="bold", class_name="text-gray-200"),
        rx.text("Create stunning marketing visuals with our AI-powered drag-and-drop editor.", text_align="center", class_name="text-gray-400"),
        primary_button("Start Creating", rx.redirect("/editor"), icon="arrow-right"),
        spacing="6",
        align_items="center",
        justify_content="center",
        height="100vh",
        class_name="bg-gray-900",
        role="main",
        aria_label="Welcome page",
    )
