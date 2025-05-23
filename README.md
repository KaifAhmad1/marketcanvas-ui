```
marketcanvas-ui/
│
├── backend/                        # FastAPI application (API & AI Logic)
│   ├── main.py                     # FastAPI app instance, API endpoint definitions
│   ├── models.py                   # Pydantic models for data validation and serialization
│   ├── services.py                 # Business logic, AI model interactions, workflow orchestration
│   ├── templates_data/             # Stores JSON for default workflow templates
│   │   └── social_media_ad.json    # Example template file
│   ├── temp_uploads/               # Directory for storing uploaded files (for demonstration)
│   ├── .env                        # Environment variables (base URLs, NOT API keys)
│   └── requirements.txt            # Python dependencies for the backend
│
├── marketcanvas_ai_app/            # Reflex frontend application (User Interface)
│   ├── assets/                     # Static files (global CSS, images, fonts)
│   │   └── custom_styles.css       # Global and theme-related CSS
│   ├── components/                 # Reusable Reflex UI components
│   │   ├── __init__.py
│   │   ├── react_flow_custom.py    # Reflex wrapper for the ReactFlow.js library
│   │   └── ui_panels.py            # Components for Node Palette, Properties, Right Sidebar, Modals
│   ├── state/                      # Reflex state management
│   │   ├── __init__.py
│   │   └── app_state.py            # Core application state (nodes, edges, UI settings, API keys, API calls)
│   ├── marketcanvas_ai_app.py      # Main Reflex app definition, page layouts
│   ├── rxconfig.py                 # Reflex project configuration
│   └── requirements.txt            # Python dependencies for the frontend
│
├── .gitignore                      # Specifies intentionally untracked files
└── README.md                       # Project overview, setup, and usage guide
```
