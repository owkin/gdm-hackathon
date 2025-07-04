import google.auth
import google.auth.transport.requests
from smolagents import OpenAIServerModel

from gdm_hackathon.config import ENDPOINT_MODELS_DICT, GCP_PROJECT_ID, GCP_LOCATION




def get_access_token():
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    access_token = creds.token
    return access_token

def get_endpoint_url(model_name):
    if model_name not in ENDPOINT_MODELS_DICT:
        raise ValueError(f"Model {model_name} not found in ENDPOINT_MODELS_DICT. Available models: {ENDPOINT_MODELS_DICT.keys()}")
    return f"https://{ENDPOINT_MODELS_DICT[model_name]['endpoint_id']}.{GCP_LOCATION}-797788125421.prediction.vertexai.goog/v1/projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/endpoints/{ENDPOINT_MODELS_DICT[model_name]['endpoint_id']}"


def get_model(model_name):
    return OpenAIServerModel(
        model_id=ENDPOINT_MODELS_DICT[model_name]['model_id'],
        api_base=get_endpoint_url(model_name),
        api_key=get_access_token(),
    )