# frontend/components/ui_components.py
import reflex as rx
from typing import Optional, List, Dict, Any
from ..state.canvas_state import CanvasState

def primary_button(text: str, on_click=None, icon: Optional[str] = None, disabled: bool = False, variant: str = "primary", class_name: str = ""):
    content = []
    if icon:
        content.append(rx.icon(tag=icon, size=16, margin_right="0.5em"))
    content.append(rx.text(text))

    base_classes = "px-4 py-2 rounded-lg transition-all duration-300 flex items-center gap-2 shadow-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed animate-fade-in"

    variant_classes = {
        "primary": "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700",
        "secondary": "bg-gray-600 text-white hover:bg-gray-700",
        "success": "bg-green-600 text-white hover:bg-green-700",
        "danger": "bg-red-600 text-white hover:bg-red-700",
        "warning": "bg-yellow-600 text-white hover:bg-yellow-700",
        "outline": "border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white"
    }

    return rx.button(
        *content,
        on_click=on_click if on_click else lambda: None,
        disabled=disabled,
        class_name=f"{base_classes} {variant_classes.get(variant, variant_classes['primary'])} {class_name}",
    )

def icon_button(icon: str, on_click=None, tooltip: str = "", size: str = "md", class_name: str = "", variant: str = "solid"):
    sizes = {
        "sm": {"icon": 14, "padding": "p-1.5"},
        "md": {"icon": 16, "padding": "p-2"},
        "lg": {"icon": 20, "padding": "p-2.5"}
    }

    size_config = sizes.get(size, sizes["md"])
    variant_classes = {
        "solid": "bg-gray-700 hover:bg-gray-600 text-gray-200",
        "ghost": "bg-transparent hover:bg-gray-600 text-gray-200"
    }

    return rx.button(
        rx.icon(tag=icon, size=size_config["icon"]),
        on_click=on_click if on_click else lambda: None,
        class_name=f"{variant_classes.get(variant, variant_classes['solid'])} rounded-lg transition-all duration-300 hover:scale-110 {size_config['padding']} {class_name} animate-fade-in",
        title=tooltip
    )

def color_picker(value: str, on_change=None):
    return rx.box(
        rx.input(
            type="color",
            value=value,
            on_change=on_change,
            class_name="w-8 h-8 rounded-full border-none cursor-pointer"
        ),
        class_name="relative"
    )

def modal(title: str, content: rx.Component, is_open: rx.Var[bool], on_close, size: str = "md"):
    size_classes = {
        "sm": "max-w-sm",
        "md": "max-w-md",
        "lg": "`max-w-lg",
        "xl": "max-w-xl",
        "2xl": "max-w-2xl",
        "full": "max-w-full mx-4"
    }

    return rx.dialog.root(
        rx.dialog.trigger(rx.box()),
        rx.dialog.portal(
            rx.dialog.overlay(class_name="fixed inset-0 bg-black bg-opacity-75 z-40 animate-fade-in"),
            rx.dialog.content(
                rx.dialog.title(title, class_name="text-xl font-semibold text-white mb-4"),
                content,
                rx.dialog.close(
                    icon_button("x", on_click=on_close, tooltip="Close", class_name="absolute top-3 right-3")
                ),
                class_name=f"fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800 border border-gray-700 rounded-lg p-6 {size_classes.get(size, size_classes['md'])} w-full space-y-4 max-h-[90vh] overflow-y-auto z-50 shadow-2xl animate-slide-in",
            ),
        ),
        open=is_open,
        on_open_change=lambda open_state: on_close() if not open_state else None
    )

def card(children: List[rx.Component], title: str = "", class_name: str = ""):
    content = []
    if title:
        content.append(rx.heading(title, size="5", class_name="mb-4 text-white"))
    content.extend(children)

    return rx.box(
        *content,
        class_name=f"bg-gray-800 border border-gray-700 rounded-lg p-6 shadow-lg hover:shadow-xl transition-all duration-300 {class_name} animate-fade-in"
    )

def sidebar_panel(title: str, children: List[rx.Component], is_open: rx.Var[bool] = rx.Var.create(True)):
    return rx.cond(
        is_open,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading(title, size="6", class_name="text-white"),
                    icon_button(
                        "chevron-left",
                        on_click=lambda: setattr(CanvasState, f"show_{title.lower()}_panel", False),
                        tooltip="Collapse",
                        size="sm",
                        class_name="ml-auto"
                    ),
                    width="100%",
                    align_items="center"
                ),
                *children,
                spacing="4",
                class_name="h-full"
            ),
            class_name="w-80 bg-gray-800 border-r border-gray-700 p-6 h-full overflow-y-auto transition-all duration-300 animate-slide-in"
        ),
        rx.box(
            icon_button(
                "chevron-right",
                on_click=lambda: setattr(CanvasState, f"show_{title.lower()}_panel", True),
                tooltip="Expand"
            ),
            class_name="w-12 bg-gray-800 border-r border-gray-700 flex items-center justify-center h-full"
        )
    )

def progress_bar(value: int, max_value: int = 100, color: str = "blue", show_text: bool = True):
    percentage = min(100, max(0, (value / max_value) * 100))

    color_classes = {
        "blue": "bg-blue-600",
        "green": "bg-green-600",
        "red": "bg-red-600",
        "yellow": "bg-yellow-600",
        "purple": "bg-purple-600"
    }
    
    radix_color_map = {
        "blue": "blue", "green": "green", "red": "red", "yellow": "amber", "purple": "purple"
    }

    progress_component = rx.progress(
        value=int(percentage), 
        color_scheme=radix_color_map.get(color, "blue"), 
        size="2",
        width="100%",
        class_name="transition-all duration-500"
    )

    content = [progress_component]

    if show_text:
        content.append(
            rx.text(f"{value}/{max_value} ({percentage:.0f}%)", color_scheme="gray", class_name="text-xs mt-1")
        )

    return rx.vstack(*content, spacing="1", width="100%")

def toast_notification(message: str, type: str = "info", duration: int = 3000):
    type_classes = {
        "info": "bg-blue-600 border-blue-500",
        "success": "bg-green-600 border-green-500",
        "warning": "bg-yellow-600 border-yellow-500",
        "error": "bg-red-600 border-red-500"
    }
    icon_map = {
        "info": "info", "success": "check-circle-2", "warning": "alert-triangle", "error": "x-circle"
    }

    return rx.box(
        rx.hstack(
            rx.icon(tag=icon_map.get(type, "info"), size=20),
            rx.text(message, class_name="text-white"),
            spacing="3",
            align="center"
        ),
        class_name=f"fixed top-4 right-4 {type_classes.get(type, type_classes['info'])} border rounded-lg p-4 shadow-lg z-[100] animate-slide-in",
        style={"animationDuration": f"{duration}ms"}
    )
