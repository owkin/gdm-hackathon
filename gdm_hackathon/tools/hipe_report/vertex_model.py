#!/usr/bin/env python3
"""
Custom Vertex AI Model for smolagents

This module provides a custom model class that can be used with smolagents
to connect to Vertex AI endpoints instead of using the default InferenceClientModel.
"""

import os
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from smolagents.models.base import BaseModel


class VertexAIModel(BaseModel):
    """
    Custom model class for smolagents that uses Vertex AI endpoints.
    
    This class implements the BaseModel interface required by smolagents
    and provides methods to interact with Vertex AI endpoints.
    """
    
    def __init__(
        self,
        endpoint_id: str,
        endpoint_region: str,
        project_id: Optional[str] = None,
        max_tokens: int = 800,
        temperature: float = 0.0,
        use_dedicated_endpoint: bool = True
    ):
        """
        Initialize the Vertex AI model.
        
        Args:
            endpoint_id: The Vertex AI endpoint ID
            endpoint_region: The region where the endpoint is deployed
            project_id: Google Cloud project ID. If None, uses GOOGLE_CLOUD_PROJECT env var
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 for deterministic)
            use_dedicated_endpoint: Whether using a dedicated endpoint
        """
        self.endpoint_id = endpoint_id
        self.endpoint_region = endpoint_region
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.use_dedicated_endpoint = use_dedicated_endpoint
        
        # Get project ID
        if project_id is None:
            self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "gemma-hcls25par-703")
            if not self.project_id:
                raise ValueError("Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable")
        else:
            self.project_id = project_id
        
        # Initialize Vertex AI
        aiplatform.init(project=self.project_id, location=self.endpoint_region)
        
        # Create endpoint object
        self.endpoint = aiplatform.Endpoint(
            endpoint_name=self.endpoint_id,
            project=self.project_id,
            location=self.endpoint_region,
        )
        
        print(f"[VertexAIModel] Initialized with endpoint: {self.endpoint_id} in {self.endpoint_region}")
    
    def generate(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """
        Generate a response using the Vertex AI endpoint.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional arguments (max_tokens, temperature, etc.)
        
        Returns:
            Generated text response
        """
        # Extract parameters
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        temperature = kwargs.get('temperature', self.temperature)
        
        # Convert messages to a single prompt
        prompt = self._messages_to_prompt(messages)
        
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
            # Make prediction
            response = self.endpoint.predict(
                instances=instances, 
                use_dedicated_endpoint=self.use_dedicated_endpoint
            )
            
            return response.predictions[0]
            
        except Exception as e:
            print(f"[VertexAIModel] Error during generation: {e}")
            return f"Error: API call failed. Details: {e}"
    
    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """
        Convert a list of messages to a single prompt string.
        
        Args:
            messages: List of message dictionaries
        
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"User: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
            else:
                prompt_parts.append(content)
        
        return "\n".join(prompt_parts)
    
    def __call__(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """
        Callable interface for the model.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional arguments
        
        Returns:
            Generated text response
        """
        return self.generate(messages, **kwargs)


def create_vertex_model(
    endpoint_id: str = "4761133837897957376",
    endpoint_region: str = "europe-west4",
    project_id: Optional[str] = None,
    max_tokens: int = 800,
    temperature: float = 0.0
) -> VertexAIModel:
    """
    Factory function to create a Vertex AI model instance.
    
    Args:
        endpoint_id: The Vertex AI endpoint ID
        endpoint_region: The region where the endpoint is deployed
        project_id: Google Cloud project ID
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature
    
    Returns:
        Configured VertexAIModel instance
    """
    return VertexAIModel(
        endpoint_id=endpoint_id,
        endpoint_region=endpoint_region,
        project_id=project_id,
        max_tokens=max_tokens,
        temperature=temperature
    ) 