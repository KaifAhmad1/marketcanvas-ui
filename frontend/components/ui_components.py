import reflex as rx
from typing import Optional, List, Dict, Any

def primary_button(text: str, on_click=None, icon: str = None, disabled: bool = False, variant: str = "primary"):
    content = []
    if icon:
        content.append(rx.icon(tag=icon, size=16))
    content.append(rx.text(text))
    
    base_classes = "px-4 py-2 rounded-lg transition-all duration-200 flex items-center gap-2 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
    
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
        class_name=f"{base_classes} {variant_classes.get(variant, variant_classes['primary'])}",
    )

def icon_button(icon: str, on_click=None, tooltip: str = "", size: str = "md"):
    sizes = {
        "sm": {"icon": 14, "padding": "p-2"},
        "md": {"icon": 16, "padding": "p-3"},
        "lg": {"icon": 20, "padding": "p-4"}
    }
    
    size_config = sizes.get(size, sizes["md"])
    
    return rx.button(
        rx.icon(tag=icon, size=size_config["icon"]),
        on_click=on_click if on_click else lambda: None,
        class_name=f"bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-all duration-200 {size_config['padding']}",
        title=tooltip
    )

def modal(title: str, content: rx.Component, is_open: rx.Var[bool], on_close, size: str = "md"):
    size_classes = {
        "sm": "max-w-sm",
        "md": "max-w-md", 
        "lg": "max-w-lg",
        "xl": "max-w-xl",
        "2xl": "max-w-2xl",
        "full": "max-w-full mx-4"
    }
    
    return rx.cond(
        is_open,
        rx.box(
            rx.box(
                rx.box(
                    rx.hstack(
                        rx.heading(title, size="lg", color="white"),
                        icon_button("x", on_close, "Close"),
                        justify="space-between",
                        width="100%",
                        align="center"
                    ),
                    content,
                    class_name=f"bg-gray-800 border border-gray-700 rounded-lg p-6 {size_classes.get(size, size_classes['md'])} w-full space-y-4 max-h-[90vh] overflow-y-auto",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50 p-4",
            ),
            class_name="fixed inset-0 bg-black bg-opacity-75 z-40",
            on_click=on_close
        ),
        rx.box(),
    )

def card(children: List[rx.Component], title: str = "", className: str = ""):
    content = []
    if title:
        content.append(rx.heading(title, size="md", color="white", class_name="mb-4"))
    content.extend(children)
    
    return rx.box(
        *content,
        class_name=f"bg-gray-800 border border-gray-700 rounded-lg p-6 shadow-lg {className}"
    )

def sidebar_panel(title: str, children: List[rx.Component], is_open: rx.Var[bool] = True):
    return rx.cond(
        is_open,
        rx.box(
            rx.vstack(
                rx.heading(title, size="lg", color="white", class_name="mb-4"),
                *children,
                spacing="4",
                class_name="h-full"
            ),
            class_name="w-80 bg-gray-800 border-r border-gray-700 p-6 h-full overflow-y-auto"
        ),
        rx.box(class_name="w-12 bg-gray-800 border-r border-gray-700")
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
    
    content = [
        rx.box(
            rx.box(
                class_name=f"{color_classes.get(color, color_classes['blue'])} h-full rounded transition-all duration-300",
                style={"width": f"{percentage}%"}
            ),
            class_name="w-full bg-gray-700 rounded h-3 overflow-hidden"
        )
    ]
    
    if show_text:
        content.append(
            rx.text(f"{value}/{max_value} ({percentage:.1f}%)", 
                   class_name="text-sm text-gray-400 mt-1")
        )
    
    return rx.vstack(*content, spacing="1")

def toast_notification(message: str, type: str = "info", duration: int = 3000):
    type_classes = {
        "info": "bg-blue-600 border-blue-500",
        "success": "bg-green-600 border-green-500",
        "warning": "bg-yellow-600 border-yellow-500", 
        "error": "bg-red-600 border-red-500"
    }
    
    return rx.box(
        rx.hstack(
            rx.icon(tag="info", size=20),
            rx.text(message, color="white"),
            spacing="3",
            align="center"
        ),
        class_name=f"fixed top-4 right-4 {type_classes.get(type, type_classes['info'])} border rounded-lg p-4 shadow-lg z-50 animate-slide-in"
    )

def dropdown_menu(trigger_text: str, items: List[Dict[str, Any]], on_select=None):
    return rx.menu(
        rx.menu_button(
            rx.button(
                trigger_text,
                rx.icon(tag="chevron-down", size=16),
                class_name="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
            )
        ),
        rx.menu_list(
            *[
                rx.menu_item(
                    item["label"],
                    on_click=lambda item=item: on_select(item["value"]) if on_select else None
                )
                for item in items
            ],
            class_name="bg-gray-800 border border-gray-700 rounded-lg shadow-lg"
        )
    )

def tabs(tabs_data: List[Dict[str, Any]], active_tab: str, on_tab_change=None):
    return rx.tabs(
        rx.tab_list(
            *[
                rx.tab(
                    tab["label"],
                    value=tab["value"],
                    class_name="px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent hover:border-blue-500 data-[selected]:border-blue-500 data-[selected]:text-white"
                )
                for tab in tabs_data
            ],
            class_name="flex border-b border-gray-700"
        ),
        *[
            rx.tab_panel(
                tab["content"],
                value=tab["value"],
                class_name="p-4"
            )
            for tab in tabs_data
        ],
        value=active_tab,
        on_change=on_tab_change
    )
