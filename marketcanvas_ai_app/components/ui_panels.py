import reflex as rx
from ..state.app_state import AppState, StylePreset, WorkflowTemplate, NodeData

# --- Node Palette Configurations ---
AVAILABLE_NODES_CONFIG = {
    "imageUpload": {"label": "Upload Image", "icon": "upload_file", "color_scheme": "blue", "description": "Upload an image from your device."},
    "imageInput": {"label": "Image URL", "icon": "link", "color_scheme": "cyan", "description": "Input an image via public URL."},
    "textToImage": {"label": "AI Text-to-Image", "icon": "palette", "color_scheme": "purple", "description": "Generate images from text prompts."},
    "productInScene": {"label": "AI Product Scene", "icon": "camera_enhance", "color_scheme": "teal", "description": "Place product images into AI scenes."},
    "styleApply": {"label": "AI Style Apply", "icon": "brush", "color_scheme": "orange", "description": "Transfer artistic styles to images."},
    "cropResize": {"label": "Crop / Resize", "icon": "crop", "color_scheme": "green", "description": "Basic image transformations."},
    "textOverlay": {"label": "Text Overlay", "icon": "title", "color_scheme": "pink", "description": "Add text to your visuals."},
    "outputNode": {"label": "Output Viewer", "icon": "visibility", "color_scheme": "gray", "description": "View the final or intermediate result."}
}

AI_PROVIDER_OPTIONS = [
    rx.option("Fal.ai", value="fal_ai"),
    rx.option("Google Gemini", value="google_gemini"),
    rx.option("Stability AI", value="stability_ai"),
    # rx.option("Blackforest Flux", value="blackforest_flux"), # Example for future
]

# --- Reusable Form Control Helpers ---
def _form_control_wrapper(label: str, control: rx.Component) -> rx.Component:
    return rx.form_control(
        rx.form_label(label, font_size="0.8em", margin_bottom="0.2em", color="var(--secondary-accent)"),
        control,
        width="100%", margin_bottom="0.85em"
    )

def _data_input_field(label: str, field_name: str, placeholder: str="", input_type: str="text", **props) -> rx.Component:
    return _form_control_wrapper(label, rx.input(
        value=AppState.selected_node.data.get(field_name, "" if input_type != "number" else 0),
        on_change=lambda val: AppState.update_selected_node_data(field_name, val),
        placeholder=placeholder, type=input_type, size="sm",
        bg="var(--input-bg)", border_color="var(--input-border)", color="var(--app-text-color)",
        _focus={"border_color": "var(--primary-accent)", "box_shadow": f"0 0 0 1px var(--primary-accent)"}, **props
    ))

def _data_textarea_field(label: str, field_name: str, placeholder: str="", rows: int = 3, **props) -> rx.Component:
    return _form_control_wrapper(label, rx.text_area(
        value=AppState.selected_node.data.get(field_name, ""),
        on_change=lambda val: AppState.update_selected_node_data(field_name, val),
        placeholder=placeholder, size="sm", rows=rows,
        bg="var(--input-bg)", border_color="var(--input-border)", color="var(--app-text-color)",
        _focus={"border_color": "var(--primary-accent)", "box_shadow": f"0 0 0 1px var(--primary-accent)"}, **props
    ))

def _data_select_field(label: str, field_name: str, options: list, placeholder:str="Select...", **props) -> rx.Component:
    return _form_control_wrapper(label, rx.select(
        options, value=AppState.selected_node.data.get(field_name, ""),
        on_change=lambda val: AppState.update_selected_node_data(field_name, val),
        placeholder=placeholder, size="sm",
        bg="var(--input-bg)", border_color="var(--input-border)", color="var(--app-text-color)",
        icon_color="var(--secondary-accent)",
        _focus={"border_color": "var(--primary-accent)", "box_shadow": f"0 0 0 1px var(--primary-accent)"}, **props
    ))

def _ai_provider_selector(field_name: str = "provider") -> rx.Component: # Added field_name argument
    return _data_select_field("AI Provider", field_name, AI_PROVIDER_OPTIONS, "Select AI Provider...")


# --- Left Sidebar: Node Palette & Asset Upload ---
def node_palette_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Toolbox", size="md", margin_bottom="1em", padding_x="0.75em", color="var(--app-text-color)"),
        rx.vstack(
            rx.text("Upload Image", font_weight="500", margin_bottom="0.3em", font_size="sm"),
            rx.upload(
                rx.center(
                    rx.vstack(
                        rx.icon(tag="upload_file", size="1.8em", color="var(--primary-accent)"),
                        rx.text("Click or Drag Image", font_size="xs", color="var(--secondary-accent)"),
                        spacing="1", padding_y="0.8em"
                    ),
                    height="80px", width="100%"
                ),
                id="asset_uploader_sidebar", border="2px dashed var(--border-color)", padding="0.5em",
                width="100%", border_radius="md", on_drop=AppState.handle_asset_upload,
                is_disabled=AppState.is_uploading_asset, _hover={"border_color": "var(--primary-accent)"}
            ),
            rx.cond(AppState.is_uploading_asset, rx.center(rx.circular_progress(is_indeterminate=True, size="20px", color="var(--primary-accent)"), margin_top="0.3em")),
            rx.cond(AppState.uploaded_asset_url.is_not_none() and not AppState.is_uploading_asset,
                rx.text(f"Up: {AppState.uploaded_asset_url.split('/')[-1][:20]}...", font_size="0.7em", color="var(--secondary-accent)", margin_top="0.3em", no_of_lines=1)
            ),
            spacing="1", padding_x="0.75em", margin_bottom="1em", width="100%"
        ),
        rx.text("Add Nodes", font_weight="500", margin_bottom="0.3em", font_size="sm", padding_x="0.75em"),
        rx.vstack(
            *[
                rx.button(
                    rx.hstack(rx.icon(tag=config["icon"], size="1.1em"), rx.text(config["label"], font_size="0.85em"), spacing="2", align_items="center"),
                    on_click=lambda type_key=type_key, name_prefix=config["label"]: AppState.add_node(type_key, name_prefix),
                    width="100%", justify_content="flex-start", variant="ghost",
                    color_scheme=config["color_scheme"], # Reflex uses this for some base styling
                    _hover={"background_color": rx.color(config["color_scheme"], 1)} # Use Chakra color scale
                )
                for type_key, config in AVAILABLE_NODES_CONFIG.items()
            ],
            spacing="0", padding_x="0.25em", width="100%" # Reduced spacing for denser look
        ),
        rx.divider(margin_y="1em", border_color="var(--border-color)"),
        rx.button(
            "Delete Selected",
            on_click=AppState.delete_selected_node, color_scheme="red", variant="outline",
            width="calc(100% - 1.5em)", margin_x="0.75em", size="sm",
            is_disabled=AppState.selected_node.is_none(), left_icon=rx.icon(tag="delete", size="1.1em")
        ),
        padding_y="1em", height="100%", overflow_y="auto", class_name="custom-scrollbar",
        bg="var(--panel-bg)", border_right="1px solid var(--border-color)", spacing="3", width="var(--sidebar-width-left)"
    )

# --- Center Top Area: Properties Panel ---
def _node_specific_properties_ui() -> rx.Component:
    node_type = AppState.selected_node.type
    common_props = rx.fragment(_data_input_field("Label", "label", "Node Label"))

    specific_props = rx.fragment() # Default to empty fragment
    if node_type == "imageInput":
        specific_props = _data_input_field("Image URL", "input_image_url", "https://example.com/image.jpg")
    elif node_type == "imageUpload":
        specific_props = rx.vstack(
            rx.text(f"File: {AppState.selected_node.data.get('file_name', 'N/A')}", font_size="sm"),
            rx.text(f"URL: {AppState.selected_node.data.get('output_image_url', 'N/A')}", font_size="xs", no_of_lines=1, title=AppState.selected_node.data.get('output_image_url', 'N/A')),
            align_items="flex-start", spacing="1"
        )
    elif node_type == "textToImage":
        specific_props = rx.fragment(
            _ai_provider_selector(),
            _data_textarea_field("Prompt", "prompt", "e.g., Enchanted forest at twilight"),
            _data_textarea_field("Negative Prompt", "negative_prompt", "e.g., blurry, ugly, text, watermark", rows=2),
            _data_input_field("Seed", "seed", "e.g., 12345", input_type="number")
        )
    elif node_type == "productInScene":
        specific_props = rx.fragment(
            _ai_provider_selector(), # Assuming this node could also use different backends
            _data_input_field("Base Image URL (from input or URL)", "base_image_url", "URL of background"),
            _data_input_field("Product Image URL (from input or URL)", "product_image_url", "URL of product"),
            _data_textarea_field("Integration Prompt", "prompt", "e.g., Place product on the marble table")
        )
    elif node_type == "styleApply":
        style_mode_options = [rx.option(mode.replace("_", " ").title(), value=mode) for mode in ["preset", "image_reference"]]
        preset_options = [rx.option(p.name, value=p.id) for p in AppState.available_style_presets]
        specific_props = rx.fragment(
            _ai_provider_selector(), # Assuming style models could vary by provider
            _data_select_field("Style Mode", "style_mode", style_mode_options),
            rx.cond(AppState.selected_node.data.get("style_mode") == "preset",
                _data_select_field("Style Preset", "style_preset_id", preset_options, "Select a style preset...")),
            rx.cond(AppState.selected_node.data.get("style_mode") == "image_reference",
                _data_input_field("Style Reference Image URL", "style_reference_image_url", "http://style-image.jpg")),
            _data_input_field("Intensity", "intensity", "0.7", input_type="number", step="0.05", min="0", max="1"),
        )
    elif node_type == "textOverlay":
        alignment_options = [rx.option(opt.title(), value=opt) for opt in ["left", "center", "right"]]
        specific_props = rx.fragment(
            _data_textarea_field("Text Content", "text_content", "Your overlay text", rows=2),
            _data_input_field("Font Family", "font_family", "Arial, sans-serif"),
            rx.hstack(
                _data_input_field("Font Size (px)", "font_size", "48", input_type="number", width="50%"),
                _data_input_field("Font Color", "font_color", "#FFFFFF", input_type="color", width="50%"), # Color picker
                spacing="2", width="100%"
            ),
            rx.hstack(
                _data_input_field("X Position (%)", "text_x_position_percent", "50", input_type="number", min="0", max="100", width="50%"),
                _data_input_field("Y Position (%)", "text_y_position_percent", "50", input_type="number", min="0", max="100", width="50%"),
                spacing="2", width="100%"
            ),
            _data_select_field("Text Alignment", "text_alignment", alignment_options),
            _data_input_field("Background Color (hex, optional)", "background_color", "#00000080", input_type="color"),
        )
    elif node_type == "cropResize": # Simplified
        specific_props = rx.fragment(
             _data_input_field("Resize Width (px, optional)", "resize_width", "e.g. 1024", input_type="number"),
             _data_input_field("Resize Height (px, optional)", "resize_height", "e.g. 1024", input_type="number"),
             # Add crop fields if needed: x, y, width, height
        )

    return rx.vstack(common_props, specific_props, spacing="3", width="100%", align_items="stretch")

def properties_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading(
                rx.cond(
                    AppState.selected_node.is_not_none(),
                    f"{AVAILABLE_NODES_CONFIG.get(AppState.selected_node.type, {'label': 'Node'})['label']} Properties",
                    "Properties"
                ),
                size="md", color="var(--app-text-color)"
            ),
            rx.spacer(),
            rx.cond(AppState.selected_node.is_not_none(),
                rx.text(f"ID: {AppState.selected_node.id}", font_size="0.7em", color="var(--secondary-accent)")
            ),
            padding_x="0.75em", padding_y="0.5em", width="100%",
            border_bottom="1px solid var(--border-color)", bg="var(--panel-header-bg)"
        ),
        rx.cond(
            AppState.selected_node.is_none(),
            rx.center(rx.text("Select a node to view its properties.", color="var(--secondary-accent)", padding="2em", font_style="italic")),
            rx.vstack(
                _node_specific_properties_ui(),
                rx.cond(AppState.selected_node.data.get("output_image_url", "").to(bool),
                     rx.vstack(
                        rx.text("Node Output Preview:", font_size="xs", margin_top="0.5em", font_weight="500", color="var(--secondary-accent)"),
                        rx.image(src=AppState.selected_node.data.get("output_image_url"), max_height="120px", width="auto",
                                 border="1px solid var(--border-color)", object_fit="contain", border_radius="md", bg="var(--canvas-bg)"),
                        align_items="flex-start", width="100%", margin_top="0.5em"
                    )
                ),
                rx.cond(AppState.selected_node.data.get("error_message", "").to(bool),
                    rx.box(
                        rx.hstack(rx.icon(tag="error_outline", color="var(--error-text-color)"), rx.text("Node Error:", font_weight="bold", color="var(--error-text-color)")),
                        rx.text(AppState.selected_node.data.get("error_message"), color="var(--error-text-color)", font_size="xs", white_space="pre-wrap"),
                        margin_top="0.5em", padding="0.5em", bg="var(--error-bg-color)", border_radius="md", border_left=f"3px solid var(--error-border-color)", width="100%"
                    )
                ),
                align_items="stretch", width="100%", spacing="3", padding="0.75em"
            )
        ),
        height="100%", # Take full height of its container in the right sidebar
        overflow_y="auto", class_name="custom-scrollbar", bg="var(--panel-bg)",
        spacing="0" # No space between header and content
    )

# --- Right Sidebar: Combination of Tools, Preview, Log ---
def right_sidebar_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Tools & Output", size="md", color="var(--app-text-color)"),
            rx.spacer(),
            rx.icon_button(rx.icon(tag="settings"), on_click=AppState.toggle_api_key_modal, variant="ghost", size="sm", title="Manage API Keys"),
            padding_x="0.75em", padding_y="0.5em", width="100%",
            border_bottom="1px solid var(--border-color)", bg="var(--panel-header-bg)"
        ),
        rx.tabs(
            rx.tab_list(
                rx.tab("Templates", _selected={"color": "var(--primary-accent)", "borderColor": "var(--primary-accent)"}),
                rx.tab("Output", _selected={"color": "var(--primary-accent)", "borderColor": "var(--primary-accent)"}),
                rx.tab("Log", _selected={"color": "var(--primary-accent)", "borderColor": "var(--primary-accent)"}),
                rx.tab("Assistant", _selected={"color": "var(--primary-accent)", "borderColor": "var(--primary-accent)"}),
            ),
            rx.tab_panels(
                rx.tab_panel( # Templates
                    rx.vstack(
                        rx.cond(
                            AppState.available_workflow_templates.length() > 0,
                            rx.foreach(
                                AppState.available_workflow_templates,
                                lambda template: rx.button(
                                    rx.vstack(rx.text(template.name, font_weight="500", font_size="0.85em", no_of_lines=1),
                                              rx.text(template.description or "", font_size="0.75em", color="var(--secondary-accent)", no_of_lines=2),
                                              align_items="flex-start", width="100%"),
                                    on_click=lambda: AppState.load_workflow_from_template(template.id),
                                    width="100%", variant="outline", margin_bottom="0.5em", height="auto", padding="0.5em", text_align="left",
                                    border_color="var(--border-color)", _hover={"bg": rx.color("gray", 2, alpha=True)}
                                )
                            ),
                            rx.text("No templates found.", font_size="sm", color="var(--secondary-accent)")
                        ),
                        spacing="2", width="100%"
                    )
                ),
                rx.tab_panel( # Output & Controls
                    rx.vstack(
                        rx.aspect_ratio(
                            rx.image(
                                src=AppState.live_preview_image_url,
                                fallback_src="https://via.placeholder.com/400x300.png?text=Workflow+Output",
                                border="1px solid var(--border-color)", object_fit="contain", border_radius="md", bg="var(--canvas-bg)"
                            ), ratio=16/10, width="100%", margin_bottom="1em" # Adjusted ratio
                        ),
                        rx.button(
                            "🚀 Execute Workflow", on_click=AppState.execute_workflow, is_loading=AppState.is_loading_workflow,
                            width="100%", color_scheme="green", left_icon=rx.icon(tag="play_arrow", size="1.2em")
                        ),
                        spacing="3", width="100%"
                    )
                ),
                rx.tab_panel( # Log
                    rx.vstack(
                        rx.box(
                            rx.cond(
                                AppState.workflow_execution_log.length() > 0,
                                rx.foreach(
                                    AppState.workflow_execution_log,
                                    lambda log_entry: rx.text(log_entry, font_size="0.7em", color="var(--secondary-accent)", no_of_lines=1, title=log_entry, margin_bottom="0.2em")
                                ),
                                rx.text("Log is empty.", font_size="xs", color="var(--secondary-accent)")
                            ),
                            height="200px", width="100%", overflow_y="auto", class_name="custom-scrollbar",
                            border="1px solid var(--border-color)", padding="0.5em", border_radius="md", bg="var(--canvas-bg)"
                        ),
                        rx.cond(
                            AppState.workflow_error_message.to(bool),
                            rx.box(
                                rx.text(AppState.workflow_error_message, color="var(--error-text-color)", font_weight="500", font_size="sm", white_space="pre-wrap"),
                                margin_top="0.5em", padding="0.5em", bg="var(--error-bg-color)", border_radius="md"
                            )
                        ),
                        spacing="2", width="100%"
                    )
                ),
                rx.tab_panel( # AI Assistant
                    rx.vstack(
                        rx.text_area(placeholder="Ask AI for workflow suggestions or help...", size="sm", bg="var(--input-bg)", margin_bottom="0.5em",
                                     on_key_down=lambda e: rx.cond(e == "Enter", AppState.fetch_ai_suggestion(e.target.value), None)), # Example on Enter
                        rx.button("Get Suggestion", on_click=lambda: AppState.fetch_ai_suggestion(), # Or use a button
                                   is_loading=AppState.is_loading_suggestion, size="sm", variant="outline", width="100%"),
                        rx.cond(AppState.is_loading_suggestion, rx.center(rx.circular_progress(is_indeterminate=True, size="20px", color="var(--primary-accent)"))),
                        rx.cond(
                            AppState.ai_assistant_suggestion.to(bool),
                            rx.box(
                                rx.markdown(AppState.ai_assistant_suggestion, component_map={"p": lambda **props: rx.text(**props, font_size="sm", white_space="pre-wrap")}), # Render markdown
                                padding="0.75em", bg=rx.color("blue", 1, alpha=True), border_radius="md",
                                border_left=f"3px solid var(--primary-accent)", width="100%", margin_top="0.5em"
                            )
                        ),
                        spacing="2", width="100%"
                    )
                ),
                padding="0.75em", width="100%", flex_grow="1", overflow_y="auto", class_name="custom-scrollbar"
            ),
            width="100%", variant="line", color_scheme="gray", is_fitted=True # Tabs styling
        ),
        height="100%", # Take full height of its container
        overflow_y="hidden", # Let tabs panel handle scroll
        bg="var(--panel-bg)",
        border_left="1px solid var(--border-color)",
        width="var(--sidebar-width-right)",
        spacing="0" # No space between header and tabs
    )

# --- API Key Input Modal ---
def api_key_input_modal() -> rx.Component:
    def key_field(provider_label: str, provider_key_name: str, placeholder_suffix: str = "API Key") -> rx.Component:
        return rx.form_control(
            rx.form_label(provider_label, font_size="sm"),
            rx.input(
                type="password", value=getattr(AppState.api_keys, provider_key_name, ""),
                on_change=lambda val: AppState.set_api_key(provider_key_name, val),
                placeholder=f"Enter {placeholder_suffix}", size="sm", width="100%",
                bg="var(--input-bg)", border_color="var(--input-border)", color="var(--app-text-color)"
            ), width="100%", margin_bottom="1em"
        )
    return rx.modal(
        rx.modal_overlay(bg=rx.color("black", alpha=0.5)),
        rx.modal_content(
            rx.modal_header(rx.text("Manage AI Provider API Keys", font_weight="600")),
            rx.modal_body(
                rx.vstack(
                    rx.text("Keys are stored in your browser for this session and sent to the backend only when needed. They are not saved on the server.",
                            font_size="xs", color="var(--secondary-accent)", margin_bottom="1.5em", font_style="italic"),
                    key_field("Fal.ai", "fal_ai_key"),
                    key_field("Google Gemini", "google_gemini_key"),
                    key_field("Stability AI", "stability_ai_key"),
                    key_field("Pipecat AI (Assistant)", "pipecat_api_key"),
                    # key_field("Blackforest Flux", "blackforest_flux_key"),
                    align_items="stretch", spacing="3"
                )
            ),
            rx.modal_footer(
                rx.button("Close", on_click=AppState.toggle_api_key_modal, variant="outline", size="sm"),
                # Optionally add a "Save to Session" button if implementing sessionStorage persistence
            ),
            bg="var(--panel-bg)", border_radius="lg", max_width="550px"
        ),
        is_open=AppState.show_api_key_modal,
        on_close=AppState.toggle_api_key_modal,
        size="xl", scroll_behavior="inside", is_centered=True
    )
