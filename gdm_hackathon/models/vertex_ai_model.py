"""Vertex AI Model for ToolCallingAgent

This model connects to a Vertex AI endpoint using the Google Cloud AI Platform SDK.
Designed to work with ToolCallingAgent which uses JSON-based tool calls.
"""

from smolagents.models import ApiModel, ChatMessage, TokenUsage
from google.cloud import aiplatform
import json
import re


class VertexAIServerModel(ApiModel):
    """This model connects to a Vertex AI endpoint using the Google Cloud AI Platform SDK."""

    def __init__(
        self, model_id: str, project_id: str, location: str, endpoint_id: str, **kwargs
    ):
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Store endpoint info for client creation
        self.project_id = project_id
        self.location = location
        self.endpoint_id = endpoint_id
        
        # Initialize parent class
        super().__init__(model_id=model_id, **kwargs)

    def create_client(self):
        """Create a Vertex AI endpoint client."""
        return aiplatform.Endpoint(
            endpoint_name=self.endpoint_id,
            project=self.project_id,
            location=self.location,
        )

    def generate(
        self,
        messages,
        stop_sequences=None,
        response_format=None,
        tools_to_call_from=None,
        **kwargs,
    ):
        """Generate a response using the Vertex AI endpoint."""
        # Use parent class to prepare completion kwargs
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            tools_to_call_from=tools_to_call_from,
            **kwargs,
        )
        
        # Extract the messages and other parameters
        messages_dict = completion_kwargs.pop("messages")
        max_tokens = completion_kwargs.get('max_tokens', 800)
        temperature = completion_kwargs.get('temperature', 0.0)
        
        # Convert messages to a simple prompt string
        prompt_parts = []
        for msg in messages_dict:
            prompt_parts.append(f"{msg['role'].title()}: {msg['content']}")
        prompt_parts.append("<start_of_turn>model")
        
        prompt = "\n".join(prompt_parts)
        
        # Create instances for prediction
        instances = [
            {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "raw_response": True,
            },
        ]
        
        # Make prediction
        response = self.client.predict(
            instances=instances, 
            use_dedicated_endpoint=True
        )
        
        # Extract the generated text
        generated_text = response.predictions[0]
        
        # Try to extract JSON tool call from the response, seems necessary for non-coding models (e.g medgemma)
        tool_call = self._extract_tool_call(generated_text)
        
        # Estimate token usage (rough approximation)
        input_tokens = len(prompt.split())
        output_tokens = len(generated_text.split())
        
        self._last_input_token_count = input_tokens
        self._last_output_token_count = output_tokens
        
        # Create ChatMessage with tool call if found
        if tool_call:
            from smolagents.models import ChatMessageToolCall, ChatMessageToolCallFunction
            return ChatMessage(
                role="assistant",
                content=None,
                tool_calls=[ChatMessageToolCall(
                    function=ChatMessageToolCallFunction(
                        name=tool_call["name"],
                        arguments=tool_call["arguments"]
                    ),
                    id="call_1",
                    type="function"
                )],
                raw=response,
                token_usage=TokenUsage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                ),
            )
        else:
            return ChatMessage(
                role="assistant",
                content=generated_text,
                raw=response,
                token_usage=TokenUsage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                ),
            )

    def _extract_tool_call(self, text: str) -> dict | None:
        try:
            # Find all code blocks labeled as tool_code or json
            code_blocks = re.findall(r'```(?:tool_code|json)\s*(\{.*?\})\s*```', text, re.DOTALL)
            for json_str in reversed(code_blocks):  # Start from the last one
                try:
                    tool_call = json.loads(json_str)
                    if "name" in tool_call and "arguments" in tool_call:
                        return tool_call
                except Exception:
                    continue
            # Fallback: previous logic (standalone JSON objects)
            json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_block_match:
                json_str = json_block_match.group(1)
                tool_call = json.loads(json_str)
                if "name" in tool_call and "arguments" in tool_call:
                    return tool_call
            json_matches = list(re.finditer(r'\{[^{}]*"name"[^{}]*"arguments"[^{}]*\}', text))
            if json_matches:
                json_match = json_matches[-1]
                json_str = json_match.group(0)
                tool_call = json.loads(json_str)
                if "name" in tool_call and "arguments" in tool_call:
                    return tool_call
            json_matches = list(re.finditer(r'\{[^{}]*"name"[^{}]*\}', text))
            if json_matches:
                json_match = json_matches[-1]
                json_str = json_match.group(0)
                tool_call = json.loads(json_str)
                if "name" in tool_call:
                    if "arguments" not in tool_call:
                        tool_call["arguments"] = {}
                    return tool_call
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"JSON extraction error: {e}")
            print(f"Text being parsed: {text[:200]}...")
            pass
        return None
