# rxconfig.py
import reflex as rx

class Config(rx.Config):
    app_name = "frontend"
    cors_allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
config = Config()
