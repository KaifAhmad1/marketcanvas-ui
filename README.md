# 🎨 MarketCanvas AI: Intelligent Visual Marketing Workflows

**MarketCanvas AI revolutionizes how marketing visuals are created. It's an intuitive, Python-powered, node-based visual editor supercharged with AI, designed for marketers, designers, and content creators who want to produce high-impact visuals efficiently and creatively.**

Build sophisticated, AI-driven pipelines by visually connecting nodes for image generation, product placement, artistic styling, text overlays, and more. Take control of your creative process, leverage multiple AI providers, and manage your projects—all within a unified, themable web interface.

**(Conceptual - Add a GIF/Screenshot of the UI in action here if available)**

---

## ✨ Core Features

*   **🧩 Intuitive Node-Based Editor:**
    *   Visually construct complex image processing and generation workflows.
    *   Drag & drop nodes for:
        *   **Image Inputs:** Upload from device, input via public URL.
        *   **AI Generation:** Text-to-Image (multi-provider), AI Product-in-Scene.
        *   **AI Styling:** Apply predefined artistic styles or (conceptually) use image references.
        *   **Image Manipulation:** Crop/Resize (simulated), Text Overlays with font/color controls.
        *   **Output:** View final or intermediate results.
    *   Connect nodes with smart edges to define data flow.
*   **🤖 Multi-Provider AI Integration (User-Provided Keys):**
    *   **Secure Key Management:** Users input their API keys for AI services directly in the UI (stored in browser session, not on the server).
    *   **Flexible AI Choices:** Select preferred AI providers for tasks like Text-to-Image:
        *   Fal.ai (Example: Fast SDXL)
        *   Google Gemini (Conceptual image output for demo)
        *   Stability AI (Example: SDXL)
        *   (Easily extendable for more providers like Blackforest Lab Flux, etc.)
    *   Backend orchestrates calls to the selected AI provider using the user's key for that operation.
*   **🚀 Workflow Templates & Style Presets:**
    *   **Workflow Templates:** Kickstart projects with pre-built node graphs for common use-cases (e.g., "Social Media Ad Post").
    *   **Style Presets:** Quickly apply predefined artistic looks (e.g., "Vintage", "Neon Glow", "Vibrant HD") to your images via a dedicated Style node.
*   **🎨 Customizable UI & Theming:**
    *   **Light & Dark Modes:** Switch between UI themes for optimal viewing comfort.
    *   Clean, modern, and responsive interface built entirely in Python with [Reflex](https://reflex.dev/).
*   **🖼️ Real-time Previews & Detailed Properties:**
    *   **Live Output:** View the output of the entire workflow or (conceptually) individual nodes.
    *   **Node Inspector:** Select any node to view and edit its specific parameters (prompts, URLs, style settings, text content, AI provider choice, etc.).
*   **🧠 AI Assistant (Conceptual):**
    *   Get contextual suggestions for workflow improvements or creative ideas.
    *   (Placeholder functionality, can be integrated with LLMs via [Pipecat.ai](https://pipecat.ai/) or other services, using user-provided API keys).
*   **⬆️ Local Asset Uploads:**
    *   Easily upload your product images or base images directly from your device to use as inputs.
*   **📊 Execution Log & Error Reporting:**
    *   Track the step-by-step execution of your workflow in a dedicated log panel.
    *   Clear error messages on nodes and in the log to help diagnose issues.
*   **⌨️ Interactive Canvas:**
    *   Drag, select, connect, and delete nodes and edges.
    *   Canvas controls for zoom and (conceptually) minimap.
    *   Snap-to-grid functionality for organized layouts.

---

## 🛠️ Technology Stack

*   **Frontend (Web UI):**
    *   [**Reflex**](https://reflex.dev/): Pure Python framework for building interactive web applications.
    *   **Node-Based Canvas:** [**ReactFlow.js**](https://reactflow.dev/): Industry-standard JavaScript library for node editors, wrapped as a custom Reflex component.
*   **Backend (API & Orchestration):**
    *   [**FastAPI**](https://fastapi.tiangolo.com/): High-performance Python framework for building robust APIs.
    *   **Pydantic:** For data validation and settings management.
*   **AI Model Integration (Examples - User provides keys):**
    *   [**Fal.ai**](https://fal.ai/): Serverless GPU for running various open-source and custom AI models.
    *   [**Google Gemini API**](https://ai.google.dev/): Access to Google's multimodal AI models.
    *   [**Stability AI API**](https://platform.stability.ai/): Access to Stable Diffusion models.
    *   *(Designed to be extendable to other providers like Blackforest Lab Flux, etc.)*
*   **Multimodal/Agent Framework (Conceptual for AI Assistant):**
    *   [**Pipecat.ai**](https://pipecat.ai/): For building conversational AI agents that can coordinate complex tasks.
*   **HTTP Client (Frontend & Backend):**
    *   [**HTTPX**](https://www.python-httpx.org/): Modern, async-capable HTTP client.
*   **File Handling (Backend):**
    *   [**AIOFiles**](https://github.com/Tinche/aiofiles): For asynchronous file operations (uploads).

---

## 🚀 Getting Started

### Prerequisites

*   **Python:** Version 3.8 or higher.
*   **Virtual Environments:** Recommended (e.g., `venv`).
*   **(Optional but Recommended for deeper JS customization of ReactFlow):** Node.js and npm/yarn.
*   **API Keys:** You will need to obtain API keys from the AI service providers you wish to use (Fal.ai, Google, Stability AI, etc.). These are entered directly into the UI.

### Installation & Running

1.  **Clone the Repository:**
    ```bash
    git clone https://your-repository-url/marketcanvas_ai_project.git
    cd marketcanvas_ai_project
    ```

2.  **Backend Setup (Terminal 1):**
    ```bash
    cd backend
    python -m venv venv_backend
    source venv_backend/bin/activate  # On Windows: venv_backend\Scripts\activate
    pip install -r requirements.txt

    # Create a .env file in the `backend` directory:
    # BACKEND_BASE_URL="http://localhost:8000"
    # TEMP_UPLOAD_DIR="temp_uploads"

    mkdir temp_uploads # Create the directory for uploads (if it doesn't exist)
    uvicorn main:app --reload --port 8000
    ```
    *The backend will start, typically on `http://localhost:8000`.*

3.  **Frontend Setup (Terminal 2):**
    ```bash
    cd marketcanvas_ai_project/marketcanvas_ai_app
    python -m venv venv_frontend
    source venv_frontend/bin/activate # On Windows: venv_frontend\Scripts\activate
    pip install -r requirements.txt
    reflex run
    ```
    *The Reflex frontend will compile and start, typically accessible at `http://localhost:3000`.*

4.  **Using the Application:**
    *   Open `http://localhost:3000` in your web browser.
    *   Click the "Settings" icon (⚙️) or "Manage API Keys" button in the UI to enter your API keys for the desired AI services.
    *   For AI-powered nodes (e.g., "Text-to-Image"), select your preferred "AI Provider" in its properties panel.
    *   Explore workflow templates, add nodes, connect them, and execute your visual generation workflows!

---

## 📁 Project Structure Overview




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
