import reflex as rx
from ..components.canvas_components import canvas, canvas_toolbar
from ..components.property_panel import property_panel
from ..components.preview_panel import preview_panel
from ..components.style_tone_editor import style_tone_editor
from ..components.llm_selector import llm_selector
from ..components.theme_builder import theme_builder
from ..components.tutorial_manager import tutorial_manager
from ..components.ab_testing import ab_testing_panel
from ..components.collaboration import collaboration_panel
from ..components.template_selector import template_selector
from ..components.analytics_dashboard import analytics_dashboard

def editor():
    return rx.vstack(
        canvas_toolbar(),
        rx.hstack(
            rx.vstack(
                llm_selector(),
                theme_builder(),
                style_tone_editor(),
                collaboration_panel(),
                template_selector(),
                analytics_dashboard(),
                spacing="4",
            ),
            canvas(),
            rx.vstack(
                property_panel(),
                preview_panel(),
                ab_testing_panel(),
                spacing="4",
            ),
            spacing="4",
            width="100%",
            height="calc(100vh - 4rem)",
        ),
        tutorial_manager(),
        padding="1rem",
        width="100%",
        class_name="bg-gray-900",
        role="main",
        aria_label="Editor page",
    )
