#!/usr/bin/env python3
"""
Heatmap Report Generation Tool using smolagents

This tool loads heatmap images from Google Storage bucket, describes them using
the medgemma-4b multimodal model, and saves the descriptions back to the bucket.
"""
# %%

import gcsfs
from PIL import Image
from io import BytesIO
import json
import base64
import requests
from datetime import datetime
from gdm_hackathon.config import GCP_PROJECT_ID
from gdm_hackathon.models.vertex_models import get_access_token, get_endpoint_url, MODELS_DICT

MODEL="gemma-3-27b"


def generate_heatmap_description(patient_id: str, feature: str, reference_features: list | None = None) -> str:
    """
    Load heatmap images for a patient/feature tuple plus reference features, describe the main feature
    using medgemma-4b, and save the description to the bucket.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'CH_B_041')
        feature: The feature name to analyze (e.g., 'TP53')
        reference_features: List of reference features to provide context (e.g., ['Malignant_bladder', 'Plasma'])
                           Defaults to ['Malignant_bladder', 'Muscle'] if None
        
    Returns:
        A success message with the saved description path
        
    Example:
        >>> generate_heatmap_description("CH_B_041", "TP53")
        "Description saved to gs://gdm-hackathon/data/descriptions/CH_B_041_TP53_description.json"
        
        >>> generate_heatmap_description("CH_B_041", "TP53", ["Malignant_bladder", "Muscle"])
        "Description saved to gs://gdm-hackathon/data/descriptions/CH_B_041_TP53_description.json"
    """
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        bucket_name = "gdm-hackathon"
        
        # Set default reference features if none provided
        if reference_features is None:
            reference_features = ["Malignant_bladder", "Muscle"]
        
        # Collect all images to send to the model
        images_to_analyze = []
        image_labels = []
        
        # Load the main feature image
        main_image_path = f"{bucket_name}/data/heatmaps/{patient_id}_{feature}_proportions.png"
        if not fs.exists(main_image_path):
            return f"Error: Main heatmap image not found at {main_image_path}"
        
        with fs.open(main_image_path, 'rb') as f:
            image_bytes = f.read()
        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode('utf-8')
        main_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        images_to_analyze.append(main_image)
        image_labels.append(f"Main feature: {feature}")
        
        # Load reference feature images
        for ref_feature in reference_features:
            ref_image_path = f"{bucket_name}/data/heatmaps/{patient_id}_{ref_feature}_proportions.png"
            if fs.exists(ref_image_path):
                with fs.open(ref_image_path, 'rb') as f:
                    ref_image_bytes = f.read()
                if isinstance(ref_image_bytes, str):
                    ref_image_bytes = ref_image_bytes.encode('utf-8')
                ref_image = Image.open(BytesIO(ref_image_bytes)).convert("RGB")
                images_to_analyze.append(ref_image)
                image_labels.append(f"Reference: {ref_feature}")
            else:
                print(f"Warning: Reference image not found at {ref_image_path}")
        
        # Create a prompt for describing the heatmap
        prompt = f"""
        You are a medical AI assistant analyzing heatmap visualizations for medical research and patient outcome prediction.
        
        I am providing you with multiple heatmap images for patient {patient_id}:
        - The MAIN FEATURE to analyze: {feature}
        - Reference features for context: {', '.join(reference_features)}
        
        Please focus your analysis PRIMARILY on the {feature} heatmap, but use the reference images 
        to understand the context and tissue structure.
        
        For the {feature} heatmap, please describe in detail:
        1. The overall pattern and distribution of {feature} expression
        2. Any notable clusters, gradients, or anomalies in {feature} expression
        3. The spatial organization of {feature} and what it might indicate especially in the context of the reference images
        4. How {feature} expression relates to the tissue structure shown in reference images
        5. Any specific features or characteristics that stand out for {feature}
        
        Low density areas appear in purple, high density areas appear in yellow.
        Provide a clear, detailed description that would be useful for medical analysis, 
        focusing specifically on {feature} expression patterns.
        """
        
        # Directly query the model as an OpenAI endpoint
        # Convert all PIL images to base64 for the API call
        content_items = []
        content_items.append({"type": "text", "text": prompt})
        
        for i, img in enumerate(images_to_analyze):
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            
            content_items.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_str}"
                }
            })
        
        # Create the messages for the OpenAI-compatible API
        messages = [
            {
                "role": "user",
                "content": content_items
            }
        ]
        
        # Get the API credentials and endpoint
        api_key = get_access_token()
        api_base = get_endpoint_url(MODEL)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": MODELS_DICT[MODEL]["model_id"],
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.2
        }
        
        response = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            description = result["choices"][0]["message"]["content"]
        else:
            description = f"Error: API call failed with status {response.status_code}: {response.text}"
        
        # Create the description data structure
        description_data = {
            "patient_id": patient_id,
            "feature": feature,
            "description": description,
            "main_image_path": main_image_path,
            "reference_features": reference_features,
            "generated_at": datetime.now().isoformat(),
            "model_used": " gemma-3-27b"
        }
        
        # Save the description to the bucket
        description_path = f"{bucket_name}/data/heatmaps/descriptions/{patient_id}_{feature}_description.json"
        
        with fs.open(description_path, 'w') as f:
            json.dump(description_data, f, indent=2)
        
        return f"Success! Description saved to gs://{description_path}\n\nDescription: {description[:200]}..."
        
    except Exception as e:
        return f"Error generating heatmap description for {patient_id}_{feature}: {str(e)}"


def list_patients_and_features() -> tuple[list[str], list[str]]:
    """
    List all available patients in the bucket.
    
    Returns:
        A formatted string listing all available patients
    """
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        bucket_name = "gdm-hackathon"
        patient_path = f"{bucket_name}/data/heatmaps/"
        
        if not fs.exists(patient_path):
            return [], []
        
        # List all files in the heatmap directory
        files = fs.ls(patient_path)
        
        if not files:
            return [], []
        
        # Extract patient_id and feature from filenames
        patient_info = []
        features = []
        for file_path in files:
            filename = file_path.split('/')[-1]
            if filename.endswith('_proportions.png'):
                base_name = filename.replace('_proportions.png', '')
                
                # Patient ID pattern is CH_*_*** (e.g., CH_B_041, CH_B_073)
                import re
                patient_match = re.match(r'(CH_[A-Z]_\d+)', base_name)
                
                if patient_match:
                    patient_id = patient_match.group(1)
                    if patient_id not in patient_info:
                        patient_info.append(patient_id)
                    feature = base_name[patient_match.end()+1:]
                    if feature not in features:
                        features.append(feature)
        if not patient_info:
            return [], []
        
        # Format the output
        return patient_info, features
        
    except Exception as e:
        return [], []


# %%
if __name__ == "__main__":
    # Test the tools
    print("Available patients and features:")
    print(list_patients_and_features())
    print("\n" + "="*60)
    
    # Test with a sample patient/feature
    print("Testing heatmap description generation:")
    print(generate_heatmap_description("CH_B_041", "RB1"))


# %%
    patient_ids, features = list_patients_and_features()
    for patient_id, feature in zip(patient_ids, features):
        print(f"Generating description for {patient_id} and {feature}")
        generate_heatmap_description(patient_id, feature)

# %%
