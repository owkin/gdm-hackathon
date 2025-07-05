# config.py

# --- GCP & Vertex AI Configuration ---
GCP_PROJECT_ID = "gemma-hcls25par-703"
GCP_LOCATION = "europe-west4"

ENDPOINT_MODELS_DICT= {
    "gemma-3-27b": {
        "endpoint_id": "5382630586475085824",
        "model_id": "google/gemma-3-27b-it-mg-one-click-deploy",
    },
    "medgemma-27b": {
        "endpoint_id": "6573269737961160704",
        "model_id": "google_medgemma-27b-text-it-mg-one-click-deploy",
    },
    "medgemma-4b": {
        "endpoint_id": "4761133837897957376",
        "model_id": "google_medgemma-4b-it-mg-one-click-deploy",
    },
}
