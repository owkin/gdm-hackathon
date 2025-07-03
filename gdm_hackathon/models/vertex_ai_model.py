"""Vertex AI Model

This model connects to a Vertex AI endpoint using the Google Cloud AI Platform SDK.
"""

from smolagents import Model, ChatMessage
import google.auth
import google.auth.transport.requests
import threading
import time
from typing import List, Optional, Any, Dict
from google.cloud import aiplatform
import re


class VertexAIServerModel(Model):
    """This model connects to a Vertex AI endpoint using the Google Cloud AI Platform SDK."""

    def __init__(
        self, model_id: str, project_id: str, location: str, endpoint_id: str, **kwargs
    ):
        #  Try to import dependencies
        try:
            from google.auth import default
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install 'google-auth and google-cloud-aiplatform' to use VertexAIServerModel"
            ) from None

        # Initialize parent class with any additional keyword arguments
        super().__init__(**kwargs)
        self.model_id = model_id
        self.project_id = project_id
        self.location = location
        self.endpoint_id = endpoint_id
        self.kwargs = kwargs
        self._refresh_task = None
        self._last_input_token_count = 0
        self._last_output_token_count = 0

        # Initialize credentials and set up Google Cloud authentication
        creds_and_project = default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.credentials: Any = creds_and_project[0]
        
        # Initialize Vertex AI
        aiplatform.init(project=self.project_id, location=self.location)
        
        # Create endpoint object
        self.endpoint = aiplatform.Endpoint(
            endpoint_name=self.endpoint_id,
            project=self.project_id,
            location=self.location,
        )
        
        print(f"[VertexAIServerModel] Initialized with endpoint: {self.endpoint_id} in {self.location}")

    @property
    def last_input_token_count(self) -> int:
        """Get the last input token count."""
        return self._last_input_token_count or 0

    @property
    def last_output_token_count(self) -> int:
        """Get the last output token count."""
        return self._last_output_token_count or 0

    def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: Optional[List[str]] = None,
        response_format: Optional[dict] = None,
        tools_to_call_from: Optional[List] = None,
        **kwargs,
    ) -> ChatMessage:
        """Generate a response from the model."""
        
        # Convert ChatMessage objects to dict format
        messages_dict = [msg.dict() for msg in messages]
        
        # Convert messages to a single prompt
        prompt = self._messages_to_prompt(messages_dict)
        
        # Extract parameters
        max_tokens = kwargs.get('max_tokens', self.kwargs.get('max_tokens', 800))
        temperature = kwargs.get('temperature', self.kwargs.get('temperature', 0.0))
        
        # Create instances for prediction
        instances = [
            {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "raw_response": True,
            },
        ]
        
        try:
            # Make prediction using Vertex AI endpoint
            response = self.endpoint.predict(
                instances=instances, 
                use_dedicated_endpoint=True
            )
            
            # Extract the generated text
            generated_text = response.predictions[0]
            
            # Post-process the response to convert markdown code blocks to <code> tags
            # Convert ```python to <code> and ``` to </code>
            processed_text = re.sub(r'```python\s*', '<code>\n', generated_text)
            processed_text = re.sub(r'```\s*', '</code>\n', processed_text)
            
            # Create a ChatMessage response
            message = ChatMessage(
                role="assistant",
                content=processed_text
            )
            
            # Set token counts (approximate)
            self._last_input_token_count = len(prompt.split())  # Rough approximation
            self._last_output_token_count = len(generated_text.split())  # Rough approximation
            
            return message
            
        except Exception as e:
            print(f"[VertexAIServerModel] Error during generation: {e}")
            # Return error message as ChatMessage
            return ChatMessage(
                role="assistant",
                content=f"Error: API call failed. Details: {e}"
            )

    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """
        Convert a list of messages to a single prompt string.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Formatted prompt string
        """
        # Add system instruction about using tools
        system_instruction = """You are a helpful AI assistant that can use Python tools to accomplish tasks. 

IMPORTANT: When you see a tool name like `load_hipe_report`, DO NOT redefine the function. Instead, use the existing tool by calling it directly.

CRITICAL: Always wrap your Python code in <code> tags like this:
<code>
result = load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1")
print(result)
</code>

For example, if you need to load a HIPE report, use:
<code>
result = load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1")
print(result)
</code>

Do NOT write:
<code>
def load_hipe_report(patient_id):
    # This is wrong - don't redefine the tool
    return "some data"
</code>

Always use the existing tools that are available to you and wrap your code in <code> tags."""
        
        prompt_parts = [f"System: {system_instruction}"]
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            # Handle different content types
            if isinstance(content, str):
                content_text = content
            elif isinstance(content, list):
                # Handle multimodal content (list of dicts)
                content_text = ""
                for item in content:
                    if isinstance(item, dict):
                        if 'text' in item:
                            content_text += item['text']
                        elif 'type' in item and item['type'] == 'text' and 'text' in item:
                            content_text += item['text']
            else:
                content_text = str(content)
            
            if role == 'system':
                prompt_parts.append(f"System: {content_text}")
            elif role == 'user':
                prompt_parts.append(f"User: {content_text}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content_text}")
            else:
                prompt_parts.append(content_text)
        
        return "\n".join(prompt_parts)

    def _refresh_token(self):
        """Refresh the Google Cloud token"""
        try:
            # Get a fresh request object
            request = google.auth.transport.requests.Request()
            self.credentials.refresh(request)  # type: ignore
        except Exception as e:
            print(f"Token refresh failed: {e}")

    def _start_refresh_loop(self):
        """Start the token refresh loop"""

        def refresh_loop():
            while True:
                time.sleep(3600)  # Refresh every hour
                self._refresh_token()

        self._refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self._refresh_thread.start()
