import google.auth
import google.auth.transport.requests
from smolagents import OpenAIServerModel


PROJECT_ID = "gemma-hcls25par-703"
LOCATION = "europe-west4"

MODELS_DICT= {
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


def get_access_token():
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    access_token = creds.token
    return access_token

def get_endpoint_url(model_name):
    if model_name not in MODELS_DICT:
        raise ValueError(f"Model {model_name} not found in MODELS_DICT. Available models: {MODELS_DICT.keys()}")
    return f"https://{MODELS_DICT[model_name]['endpoint_id']}.{LOCATION}-797788125421.prediction.vertexai.goog/v1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{MODELS_DICT[model_name]['endpoint_id']}"


def get_model(model_name):
    return OpenAIServerModel(
        model_id=MODELS_DICT[model_name]['model_id'],
        api_base=get_endpoint_url(model_name),
        api_key=get_access_token(),
    )