"""
This tool provides MedGemma 27B query functionality using the @tool decorator.
"""

#%%
from smolagents import tool
from gdm_hackathon.models.medgemma_query import get_survival_prediction_from_report_patient

# %%

@tool
def query_medgemma(prompt: str, max_tokens: int = 2_048, temperature: float = 0.0) -> str:
    """
    Query the MedGemma 27B model with a custom prompt for biomedical analysis.
    IMPORTANT: This tool can be used to get insights from the MedGemma model for survival prediction and medical analysis.
    
    This tool sends a prompt to the MedGemma 27B model and returns the model's response.
    The model is specialized in biomedical research and can analyze medical reports, 
    predict survival outcomes, and provide insights on various medical topics.
    
    Args:
        prompt: The prompt or medical report text to send to MedGemma 27B
        max_tokens: Maximum number of tokens to generate (default: 2048)
        temperature: Sampling temperature for response generation (default: 0.0 for deterministic)
        
    Returns:
        The model's response as a string
        
    Example:
        >>> query_medgemma("Analyze this immune infiltration report for survival prediction...")
        "Based on the immune infiltration analysis, the patient shows..."
    """
    try:
        # Use the existing function from medgemma_query
        response = get_survival_prediction_from_report_patient(
            medical_report=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            use_dedicated_endpoint=True
        )
        
        return response
        
    except Exception as e:
        return f"Error querying MedGemma 27B: {str(e)}. Please check your prompt and try again."

# %% 
if __name__ == "__main__":
    print(query_medgemma("What are the most promising biomarkers for bladder cancer survival prediction? Be specific in your answer : what pathways or genes, or histological features."))
# %%