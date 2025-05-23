import os
import httpx
import json
from typing import List, Dict, Any, Optional, Tuple, cast
from uuid import uuid4
from pathlib import Path
from .models import (
    Node, Edge, NodeType, WorkflowPayload, StylePreset, AIProviderKeyConfig,
    BaseNodeData, TextToImageNodeData, ProductInSceneNodeData, StyleNodeData,
    ImageInputNodeData, ImageUploadNodeData, CropResizeNodeData, TextOverlayNodeData,
    StyleApplicationMode
)

# Base URLs for AI Providers (examples)
FAL_BASE_URL = "https://fal.run"
GOOGLE_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
STABILITY_AI_BASE_URL = "https://api.stability.ai/v1"
# BLACKFOREST_FLUX_BASE_URL = "..." # Example

PREDEFINED_STYLES: List[StylePreset] = [
    StylePreset(id="style_vintage", name="Vintage Look", parameters={"prompt_suffix": ", vintage photo, old film grain, sepia tone"}),
    StylePreset(id="style_neon", name="Neon Glow", parameters={"prompt_suffix": ", neon lights, cyberpunk aesthetic, vibrant colors"}),
    StylePreset(id="style_watercolor", name="Watercolor Art", parameters={"prompt_suffix": ", watercolor painting, soft edges, artistic"}),
    StylePreset(id="style_vibrant_hd", name="Vibrant HD", parameters={"prompt_suffix": ", vibrant colors, sharp details, cinematic lighting, 8k"}),
    StylePreset(id="style_cinematic", name="Cinematic", parameters={"prompt_suffix": ", cinematic shot, dramatic lighting, wide angle, movie still"}),
]

def _parse_node_data_from_dict(node_type: NodeType, data_dict: Dict[str, Any]) -> BaseNodeData:
    if node_type == NodeType.TEXT_TO_IMAGE: return TextToImageNodeData(**data_dict)
    if node_type == NodeType.PRODUCT_IN_SCENE: return ProductInSceneNodeData(**data_dict)
    if node_type == NodeType.STYLE_APPLY: return StyleNodeData(**data_dict)
    if node_type == NodeType.IMAGE_INPUT: return ImageInputNodeData(**data_dict)
    if node_type == NodeType.IMAGE_UPLOAD: return ImageUploadNodeData(**data_dict)
    if node_type == NodeType.CROP_RESIZE: return CropResizeNodeData(**data_dict)
    if node_type == NodeType.TEXT_OVERLAY: return TextOverlayNodeData(**data_dict)
    return BaseNodeData(**data_dict)

async def _http_post_ai_service(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: float = 180.0) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text
        try:
            error_json = e.response.json()
            if "error" in error_json: # StabilityAI specific error structure
                error_detail = error_json["error"].get("message", error_json["error"])
            elif "message" in error_json: # Fal.ai specific error structure
                 error_detail = error_json["message"]
        except json.JSONDecodeError:
            pass # Stick with raw text
        return {"error_message": f"API Error ({e.response.status_code}): {error_detail}"}
    except httpx.RequestError as e:
        return {"error_message": f"Network request to {e.request.url} failed: {str(e)}"}
    except Exception as e:
        return {"error_message": f"Generic AI service call error: {str(e)}"}

async def _fal_ai_call(app_route: str, payload: Dict[str, Any], api_key: Optional[str]) -> Dict[str, Any]:
    if not api_key: return {"error_message": "Fal.ai API Key not provided."}
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    return await _http_post_ai_service(f"{FAL_BASE_URL}/{app_route}", headers, payload)

async def _google_gemini_call(model_id: str, prompt_text: str, api_key: Optional[str]) -> Dict[str, Any]:
    if not api_key: return {"error_message": "Google Gemini API Key not provided."}
    # This is for text generation. For image generation, Gemini requires different model and payload (e.g. multimodal)
    # This example simulates an image output for consistency.
    url = f"{GOOGLE_GEMINI_BASE_URL}/{model_id}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    result = await _http_post_ai_service(url, {}, payload, timeout=120.0)
    if result.get("error_message"): return result
    try:
        # Simplified: assuming text response, creating a placeholder image URL
        generated_text = result.get("candidates")[0].get("content").get("parts")[0].get("text", "Gemini_NoText")
        return {"images": [{"url": f"https://via.placeholder.com/512/4285F4/FFFFFF?Text=Gemini:{generated_text[:20]}"}]}
    except (IndexError, KeyError, TypeError) as e:
        return {"error_message": f"Could not parse Gemini response: {str(e)} - Response: {result}"}


async def _stability_ai_call(engine_id: str, prompt_text: str, api_key: Optional[str]) -> Dict[str, Any]:
    if not api_key: return {"error_message": "Stability AI API Key not provided."}
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json", "Content-Type": "application/json"}
    payload = {"text_prompts": [{"text": prompt_text}], "samples": 1, "steps": 30} # Example payload
    result = await _http_post_ai_service(f"{STABILITY_AI_BASE_URL}/generation/{engine_id}/text-to-image", headers, payload)
    if result.get("error_message"): return result
    try:
        # Stability AI returns base64 encoded images. For demo, return placeholder.
        # In production, save base64 to storage and return URL.
        if result.get("artifacts") and result["artifacts"][0].get("base64"):
            return {"images": [{"url": f"https://via.placeholder.com/512/10A37F/FFFFFF?Text=StabilityAI_Output"}]}
        return {"error_message": "Stability AI response did not contain image data."}
    except (IndexError, KeyError, TypeError) as e:
        return {"error_message": f"Could not parse Stability AI response: {str(e)} - Response: {result}"}

async def _process_node_internal(node: Node, inputs: Dict[str, Optional[str]], api_keys: AIProviderKeyConfig, log_func: callable) -> Node:
    node_data_obj = _parse_node_data_from_dict(node.type, node.data)
    node_data_obj.error_message = None # Clear previous errors
    provider = node_data_obj.provider or "fal_ai" # Default provider
    log_func(f"Node '{node.id}' ({node.type.value}) using provider '{provider}'. Inputs: {list(inputs.keys())}")

    output_url: Optional[str] = None
    error_msg: Optional[str] = None

    # Handle simple pass-through or local-like operations
    if node.type == NodeType.IMAGE_UPLOAD:
        output_url = node_data_obj.output_image_url
        if not output_url: error_msg = "Image not uploaded to this node yet."
    elif node.type == NodeType.IMAGE_INPUT:
        data = cast(ImageInputNodeData, node_data_obj)
        output_url = data.input_image_url
        if not output_url: error_msg = "Input Image URL is missing."
    elif node.type == NodeType.OUTPUT:
        output_url = inputs.get("default_in") # Assuming a 'default_in' handle
        if not output_url: error_msg = "Input to OutputNode is missing."
    elif node.type in [NodeType.CROP_RESIZE, NodeType.TEXT_OVERLAY]: # Simulated
        input_img = inputs.get("default_in")
        if not input_img: error_msg = f"Input image for {node.type.value} missing."
        else: output_url = f"{input_img}?sim_{node.type.value.lower()}=true" # Simulate operation

    # AI Operations
    elif node.type == NodeType.TEXT_TO_IMAGE:
        data = cast(TextToImageNodeData, node_data_obj)
        payload = {"prompt": data.prompt}
        if data.negative_prompt: payload["negative_prompt"] = data.negative_prompt
        if data.seed is not None: payload["seed"] = data.seed
        
        result: Optional[Dict[str, Any]] = None
        if provider == "fal_ai": result = await _fal_ai_call("fal-ai/fast-sdxl", payload, api_keys.fal_ai_key)
        elif provider == "google_gemini": result = await _google_gemini_call("gemini-pro", data.prompt, api_keys.google_gemini_key)
        elif provider == "stability_ai": result = await _stability_ai_call("stable-diffusion-xl-1024-v1-0", data.prompt, api_keys.stability_ai_key)
        else: error_msg = f"Unsupported AI provider for Text-to-Image: {provider}"
        
        if result:
            if result.get("images") and result["images"][0].get("url"): output_url = result["images"][0]["url"]
            else: error_msg = result.get("error_message") or "AI generation failed to return image URL."

    elif node.type == NodeType.PRODUCT_IN_SCENE:
        data = cast(ProductInSceneNodeData, node_data_obj)
        base_img = inputs.get("base_image_in") or data.base_image_url
        prod_img = inputs.get("product_image_in") or data.product_image_url
        if not base_img or not prod_img: error_msg = "Base or product image missing for composition."
        else:
            payload = {"base_image_url": base_img, "product_image_url": prod_img, "prompt": data.prompt}
            # This type of complex task is often specific. Assume Fal.ai or a dedicated model.
            result = await _fal_ai_call("your-fal-product-composition-app-route", payload, api_keys.fal_ai_key)
            if result:
                output_url = result.get("output_image_url") # Assuming this key from your Fal app
                if not output_url: error_msg = result.get("error_message") or "Product composition failed."

    elif node.type == NodeType.STYLE_APPLY:
        data = cast(StyleNodeData, node_data_obj)
        input_img = inputs.get("default_in")
        if not input_img: error_msg = "Input image for StyleApply missing."
        else:
            style_prompt_suffix = ""
            if data.style_mode == StyleApplicationMode.PRESET and data.style_preset_id:
                preset = next((s for s in PREDEFINED_STYLES if s.id == data.style_preset_id), None)
                if preset: style_prompt_suffix = preset.parameters.get("prompt_suffix", "")
            
            payload = {"image_url": input_img, "prompt": f"Apply artistic style {style_prompt_suffix}".strip(), "strength": data.intensity}
            # Assume Fal.ai or a dedicated model for style transfer. Provider selection could be added.
            result = await _fal_ai_call("your-fal-style-transfer-app-route", payload, api_keys.fal_ai_key)
            if result:
                if result.get("images") and result["images"][0].get("url"): output_url = result["images"][0]["url"]
                else: error_msg = result.get("error_message") or "Style application failed."
    else:
        error_msg = f"Node type '{node.type.value}' processing not implemented."

    node_data_obj.output_image_url = output_url
    node_data_obj.error_message = error_msg
    node.data = node_data_obj.model_dump(exclude_none=True)
    if error_msg: log_func(f"Error in Node '{node.id}': {error_msg}")
    if output_url: log_func(f"Node '{node.id}' output: {output_url[:70]}...")
    return node

def _get_execution_order(nodes: List[Node], edges: List[Edge]) -> List[str]:
    adj: Dict[str, List[str]] = {node.id: [] for node in nodes}
    in_degree: Dict[str, int] = {node.id: 0 for node in nodes}
    node_map: Dict[str, Node] = {node.id: node for node in nodes}
    for edge in edges:
        if edge.source in node_map and edge.target in node_map:
            adj[edge.source].append(edge.target)
            in_degree[edge.target] += 1
    queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
    execution_order = []
    while queue:
        u = queue.pop(0)
        execution_order.append(u)
        for v_id in adj.get(u, []):
            in_degree[v_id] -= 1
            if in_degree[v_id] == 0:
                queue.append(v_id)
    if len(execution_order) != len(nodes):
        print(f"Warning: Cycle or disconnected components. Executed: {len(execution_order)}/{len(nodes)}")
        # Add remaining nodes to process them and show errors if they are part of a cycle
        # This is a simple way, full cycle detection is more complex.
        processed_ids = set(execution_order)
        for node in nodes:
            if node.id not in processed_ids:
                execution_order.append(node.id) # Add at the end
    return execution_order

async def execute_ai_workflow(workflow: WorkflowPayload) -> Tuple[WorkflowPayload, List[str]]:
    execution_log: List[str] = []
    def log(message: str): execution_log.append(message)

    if not workflow.api_keys:
        log("Critical Error: API keys configuration missing in workflow payload.")
        for n in workflow.nodes: n.data["error_message"] = "API keys missing."
        return workflow, execution_log
    
    api_keys_config = workflow.api_keys
    nodes_map = {node.id: node for node in workflow.nodes}
    order = _get_execution_order(workflow.nodes, workflow.edges)
    log(f"Execution Order ({len(order)} nodes): {', '.join(order)}")

    node_outputs_cache: Dict[str, Dict[str, Optional[str]]] = {node_id: {} for node_id in nodes_map}
    processed_nodes_map: Dict[str, Node] = {}

    for node_id in order:
        if node_id not in nodes_map:
            log(f"Error: Node ID '{node_id}' from execution order not in workflow. Skipping.")
            continue
        
        current_node_original = nodes_map[node_id]
        # Create a copy to avoid modifying the original map during iteration if needed,
        # though we update processed_nodes_map.
        current_node_to_process = Node(**current_node_original.model_dump())


        inputs_for_current_node: Dict[str, Optional[str]] = {}
        for edge in workflow.edges:
            if edge.target == node_id:
                source_node_id = edge.source
                source_handle = edge.sourceHandle or "default_out"
                target_handle = edge.targetHandle or "default_in"
                
                cached_output = node_outputs_cache.get(source_node_id, {}).get(source_handle)
                if cached_output:
                    inputs_for_current_node[target_handle] = cached_output
                else:
                    # This might happen if source node failed or for cycles
                    source_node_in_map = processed_nodes_map.get(source_node_id) # Check if already processed
                    if source_node_in_map and source_node_in_map.data.get("output_image_url") and source_handle == "default_out":
                         inputs_for_current_node[target_handle] = source_node_in_map.data["output_image_url"]
                    else:
                        log(f"Warn: Output from '{source_node_id}.{source_handle}' not found for '{node_id}.{target_handle}'.")
        
        processed_node = await _process_node_internal(current_node_to_process, inputs_for_current_node, api_keys_config, log)
        processed_nodes_map[node_id] = processed_node
        
        # Cache output(s) of the processed node
        # Assuming most nodes have one primary output accessible via `output_image_url` mapped to "default_out"
        if processed_node.data.get("output_image_url"):
            node_outputs_cache[node_id]["default_out"] = processed_node.data["output_image_url"]
            # If nodes have multiple named output handles, the logic in _process_node_internal
            # would need to populate node.data with keys like "output_handle_name_url"
            # and this caching logic would need to read those specific keys.

    final_updated_nodes = []
    for node_in_original_payload in workflow.nodes:
        if node_in_original_payload.id in processed_nodes_map:
            final_updated_nodes.append(processed_nodes_map[node_in_original_payload.id])
        else:
            # Node was not processed (e.g., due to being unreachable or in a malformed part of graph)
            node_in_original_payload.data["error_message"] = "Node was not reached during execution."
            final_updated_nodes.append(node_in_original_payload)
            log(f"Node '{node_in_original_payload.id}' was not in the processed map.")

    workflow.nodes = final_updated_nodes
    return workflow, execution_log

async def get_ai_assistant_suggestion(workflow: Optional[WorkflowPayload] = None, user_query: Optional[str] = None) -> str:
    # This remains conceptual, as full Pipecat integration is complex.
    # If Pipecat or another LLM needs an API key, it should be in workflow.api_keys
    pipecat_key = workflow.api_keys.pipecat_api_key if workflow and workflow.api_keys else None

    if not pipecat_key and user_query: # If no key, but query, give generic advice
         return f"Consider how '{user_query}' relates to visual appeal or call to action."
    elif not pipecat_key:
        return "AI Assistant (Pipecat) API Key not provided. Please configure it in settings."

    # Simulate LLM call
    # In a real scenario: construct prompt, call Pipecat service with pipecat_key
    prompt = f"Workflow context: {len(workflow.nodes if workflow else [])} nodes. User query: '{user_query or 'general advice'}'. Suggest an improvement:"
    # response_from_llm = await call_my_llm_service(prompt, pipecat_key)
    # return response_from_llm
    return f"AI Suggestion based on '{user_query or 'workflow'}': Ensure high contrast text for readability. (Key: {'Used' if pipecat_key else 'Not Used'})"
