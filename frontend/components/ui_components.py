import reflex as rx

def primary_button(text: str, on_click: rx.EventHandler, icon: str = None):
    return rx.button(
        rx.cond(icon, rx.icon(tag=icon, size=16), rx.text()),
        text,
        on_click=on_click,
        class_name="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition flex items-center gap-2 shadow-glow",
        aria_label=text,
    )

def modal(title: str, content: rx.Component, is_open: rx.Var[bool], on_close: rx.EventHandler):
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(title, class_name="text-gray-200"),
                rx.modal_body(content),
                rx.modal_footer(
                    primary_button("Close", on_close),
                ),
                class_name="bg-gray-800 border border-gray-700 rounded-lg glass",
            ),
        ),
        is_open=is_open,
        role="dialog",
        aria_label=f"{title} modal",
    )

def toast(message: str, variant: str = "success"):
    return rx.html(f"""
        <script>
            import toast from 'react-hot-toast';
            toast.{variant}('{message}');
        </script>
    """)
