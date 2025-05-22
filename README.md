```
marketcanvas-ui/
├── frontend/
│   ├── assets/
│   │   ├── logo.png              # Light theme logo
│   │   ├── logo-dark.png         # Dark theme logo
│   ├── components/
│   │   ├── reactflow.py          # ReactFlow wrapper
│   │   ├── canvas_components.py  # Canvas UI (toolbar, minimap, grid)
│   │   ├── nodes.py              # Custom nodes (image, style, A/B, etc.)
│   │   ├── property_panel.py     # Enhanced property editor
│   │   ├── preview_panel.py      # WYSIWYG live canvas preview
│   │   ├── style_tone_editor.py  # Style and tone controls
│   │   ├── llm_selector.py       # LLM selection with parameters
│   │   ├── tutorial_manager.py   # Interactive tutorial system
│   │   ├── ab_testing.py        # A/B testing node controls
│   │   ├── ui_components.py      # Reusable UI elements
│   ├── pages/
│   │   ├── editor.py             # Main editor page
│   │   ├── welcome.py            # Onboarding page
│   ├── state/
│   │   ├── app_state.py          # Global state (theme, prefs)
│   │   ├── canvas_state.py       # Canvas state (nodes, edges, styles)
│   ├── styles/
│   │   ├── main.css              # Global dark theme styles
│   │   ├── canvas.css            # Canvas-specific styles
│   │   ├── themes.py             # Theme definitions
│   ├── tutorials/
│   │   ├── basic_workflow.json   # Tutorial for basic workflow
│   │   ├── advanced_workflow.json # Tutorial for advanced features
│   ├── frontend.py               # Main Reflex app
├── rxconfig.py                   # Reflex configuration
```
