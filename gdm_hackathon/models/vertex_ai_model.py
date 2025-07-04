"""Vertex AI Model for ToolCallingAgent

This model connects to a Vertex AI endpoint using the Google Cloud AI Platform SDK.
Designed to work with ToolCallingAgent which uses JSON-based tool calls.
"""

from smolagents.models import OpenAIServerModel
import time
import threading
import google.auth.transport.requests


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

class VertexAIServerModel(OpenAIServerModel):
    """This model connects to a Vertex AI-compatible API server."""

    def __init__(
        self, model_id: str, project_id: str = "797788125421", location: str = "europe-west4", endpoint_id: str | None = None, **kwargs
    ):
        #  Try to import dependencies
        try:
            from google.auth import default
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install 'openai, google-auth and requests' extra to use VertexAIGeminiModel as described in the official documentation: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/call-vertex-using-openai-library"
            ) from None
            
        endpoint_id = MODELS_DICT[model_id]["endpoint_id"]
        model_id = MODELS_DICT[model_id]["model_id"]

        # Initialize parent class with any additional keyword arguments
        api_base = (
            f"https://{endpoint_id}.{location}-{project_id}.prediction.vertexai.goog/v1/projects/"
            f"{project_id}/locations/{location}/endpoints/{endpoint_id}"
        )

        # Initialize credentials and set up Google Cloud authentication with required permissions
        self.credentials, _ = default()
        self._refresh_token()
        self._start_refresh_loop()
        super().__init__(model_id=model_id, api_base=api_base, api_key=self.credentials.token)

    def _refresh_token(self):
        """Refresh the Google Cloud token"""
        try:
            self.credentials.refresh(google.auth.transport.requests.Request())
            print(self.credentials.token)
        except Exception as e:
            print(f"Token refresh failed: {e}")


    def _start_refresh_loop(self):
        """Start the token refresh loop"""

        def refresh_loop():
            while True:
                time.sleep(3600)
                self._refresh_token()

        self._refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self._refresh_thread.start()
     
