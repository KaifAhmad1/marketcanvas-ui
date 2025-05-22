import reflex as rx

class AppState(rx.State):
    theme: str = "dark"
    accent_color: str = "Blue"
    user_id: str = ""
    user_name: str = "Guest"

    def set_theme(self, theme: str):
        self.theme = theme

    def set_accent_color(self, color: str):
        self.accent_color = color

    def set_user(self, user_id: str, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
