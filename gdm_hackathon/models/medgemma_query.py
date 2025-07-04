#!/usr/bin/env python3
"""
MedGemma 27B Survival Prediction Query Function

This module provides a simplified function to query the MedGemma 27B model 
for survival predictions based on medical reports.
"""

from google.cloud import aiplatform
from typing import List, Union

from gdm_hackathon.config import ENDPOINT_MODELS_DICT, GCP_PROJECT_ID, GCP_LOCATION

def get_survival_prediction_from_report_patient(
    medical_report: str,
    max_tokens: int = 800,
    temperature: float = 0.0,
    use_dedicated_endpoint: bool = True,
) -> str:
    """
    Get survival prediction from MedGemma 27B model based on a medical report.
    
    Args:
        medical_report (str): The medical report text to analyze
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Sampling temperature (0.0 for deterministic)
        use_dedicated_endpoint (bool): Whether using a dedicated endpoint
    
    Returns:
        str: Survival prediction from the model
    
    Raises:
        ValueError: If invalid parameters are provided
        Exception: If the query fails
    """
    
    # Validate inputs
    if not medical_report.strip():
        raise ValueError("Medical report cannot be empty")
    
    endpoint_id = ENDPOINT_MODELS_DICT["medgemma-27b"]["endpoint_id"]

    # Initialize Vertex AI
    aiplatform.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    
    # Create endpoint object
    endpoint = aiplatform.Endpoint(
        endpoint_name=endpoint_id,
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
    )
    
    # Get endpoint name for validation
    endpoint_name = endpoint.display_name
    
    # Validate that we're using an instruction-tuned model
    if "pt" in endpoint_name:
        raise ValueError(
            "The examples are intended to be used with instruction-tuned variants. "
            "Please use an instruction-tuned model."
        )
    
    # Survival prediction-focused system instruction
    system_instruction = (
        "You are a medical treatment specialist. Based on the following report, "
        "provide clear and concise survival prediction. "
    )
    
    return _query_vertex_ai(
            endpoint=endpoint,
            medical_report=medical_report,
            system_instruction=system_instruction,
            max_tokens=max_tokens,
            temperature=temperature,
            use_dedicated_endpoint=use_dedicated_endpoint
        )



def get_survival_prediction_batch(
    medical_reports: Union[str, List[str]],
    system_instruction,
    max_tokens: int = 800,
    temperature: float = 0.0,
    use_dedicated_endpoint: bool = True,
    batch_size: int = 10,
) -> Union[str, List[str]]:
    """
    Get survival predictions from MedGemma 27B model for a batch of medical reports.
    This function leverages the parallelization of the Vertex endpoint by submitting
    multiple prompts in a single request.
    
    Args:
        medical_reports (Union[str, List[str]]): Single medical report or list of medical reports
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Sampling temperature (0.0 for deterministic)
        use_dedicated_endpoint (bool): Whether using a dedicated endpoint
        batch_size (int): Maximum number of reports to process in a single batch
    
    Returns:
        Union[str, List[str]]: Single prediction or list of predictions
    
    Raises:
        ValueError: If invalid parameters are provided
        Exception: If the query fails
    """
    
    # Handle single report case
    if isinstance(medical_reports, str):
        return get_survival_prediction_from_report_patient(
            medical_report=medical_reports,
            max_tokens=max_tokens,
            temperature=temperature,
            use_dedicated_endpoint=use_dedicated_endpoint,
        )
    
    # Validate inputs for batch processing
    if not medical_reports:
        raise ValueError("Medical reports list cannot be empty")

    # Initialize Vertex AI
    aiplatform.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    
    # Create endpoint object
    endpoint = aiplatform.Endpoint(
        endpoint_name=ENDPOINT_MODELS_DICT["medgemma-27b"]["endpoint_id"],
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
    )
    
    # Get endpoint name for validation
    endpoint_name = endpoint.display_name
    
    # Validate that we're using an instruction-tuned model
    if "pt" in endpoint_name:
        raise ValueError(
            "The examples are intended to be used with instruction-tuned variants. "
            "Please use an instruction-tuned model."
        )
    
    # Process in batches
    all_predictions = []
    
    for i in range(0, len(medical_reports), batch_size):
        batch_reports = medical_reports[i:i + batch_size]
        
        batch_predictions = _query_vertex_ai_batch(
                endpoint=endpoint,
                medical_reports=batch_reports,
                system_instruction=system_instruction,
                max_tokens=max_tokens,
                temperature=temperature,
                use_dedicated_endpoint=use_dedicated_endpoint
            )

        
        all_predictions.extend(batch_predictions)
    
    return all_predictions


def _query_vertex_ai(
    endpoint: aiplatform.Endpoint,
    medical_report: str,
    system_instruction: str,
    max_tokens: int,
    temperature: float,
    use_dedicated_endpoint: bool
) -> str:
    """Query using Vertex AI SDK method for single report."""
    
    # Format the prompt
    formatted_prompt = f"{system_instruction} {medical_report} <start_of_image>"
    
    # Create instances for prediction
    instances = [
        {
            "prompt": formatted_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "raw_response": True,
        },
    ]
    
    # Make prediction
    response = endpoint.predict(
        instances=instances, 
        use_dedicated_endpoint=use_dedicated_endpoint
    )
    
    return response.predictions[0]


def _query_vertex_ai_batch(
    endpoint: aiplatform.Endpoint,
    medical_reports: List[str],
    system_instruction: str,
    max_tokens: int,
    temperature: float,
    use_dedicated_endpoint: bool
) -> List[str]:
    """Query using Vertex AI SDK method for batch of reports."""
    
    # Create instances for batch prediction
    instances = []
    for medical_report in medical_reports:
        formatted_prompt = f"{system_instruction} {medical_report} <start_of_image>"
        instances.append({
            "prompt": formatted_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "raw_response": True,
        })
    
    # Make batch prediction
    response = endpoint.predict(
        instances=instances, 
        use_dedicated_endpoint=use_dedicated_endpoint
    )
    
    return response.predictions

# Example usage
if __name__ == "__main__":
    # Example medical report
    sample_report = """
    # Immune Infiltration Analysis

        Based on the histological analysis of this whole slide image, I can provide the following description of the immune infiltration:

        ## Immune Cell Composition

        The slide shows significant immune cell presence with **lymphocytes** being the most abundant immune cell type:

        - **Lymphocytes**: 146,014 cells (21.1% of all cells), with a density of 730.7 cells/mm²
        - **Macrophages**: 31,244 cells (4.5% of all cells)
        - **Neutrophils**: 19,759 cells (2.9% of all cells), with a density of 98.9 cells/mm²
        - **Eosinophils**: 3,380 cells (0.5% of all cells), with a density of 16.9 cells/mm²
        - **Mast cells**: 895 cells (0.1% of all cells)

        ## Spatial Distribution and Tumor Interaction

        The immune infiltration shows interesting patterns of interaction with cancer cells:

        1. **Cancer-Immune Cell Proximity**: 
        - On average, there are 2.65 lymphocytes found within a 50μm radius of each cancer cell
        - Similarly, about 2.69 cancer cells are found within a 50μm radius of each lymphocyte
        - This balanced co-occurrence suggests moderately active immune surveillance with lymphocytes positioned in close proximity to cancer cells

        2. **Tumor Infiltrating Lymphocytes (TILs)**: 
        - The TILs diffusivity could not be calculated, potentially indicating that either:
            - The tumor regions could not be reliably identified
            - The lymphocyte infiltration pattern doesn't follow a typical infiltrative pattern
            - There may be discrete boundaries between tumor and immune cells rather than diffuse intermixing

        3. **Global Cell Context**:
        - The slide shows high fibroblast density (992.2 cells/mm²), indicating a stromal-rich microenvironment
        - Cancer cells are present at a density of 741.3 cells/mm²
        - Lymphocytes show a similar density (730.7 cells/mm²) to cancer cells, suggesting substantial immune presence

        ## Summary

        The immune infiltration in this sample is characterized by a lymphocyte-predominant immune response with moderate interaction between immune and cancer cells. 
        Lymphocytes comprise over 20% of all cells and are found in close proximity to cancer cells, suggesting an active immune response. There is also notable presence of 
        macrophages, neutrophils, and other immune cells, indicating a diverse immune microenvironment. 

        The balanced co-occurrence between lymphocytes and cancer cells suggests neither extreme exclusion nor overwhelming infiltration, but rather a moderate level of 
        immune-tumor interaction. The high density of fibroblasts alongside immune cells indicates a complex tumor microenvironment with potential stromal barriers that may 
        influence immune cell infiltration and function.
    """
    

    
    try:
        # Get survival prediction for single report
        prediction_response = get_survival_prediction_from_report_patient(
            medical_report=sample_report,
            )
        print("Survival Prediction (Single):")
        print(prediction_response)

        system_instruction = (
            "You are a medical treatment specialist. Based on the following report, "
            "provide clear and concise survival prediction"
        )
        # Get survival predictions for batch of reports
        sample_reports = [sample_report, sample_report, sample_report]  # Example with 3 identical reports
        batch_predictions = get_survival_prediction_batch(
            medical_reports=sample_reports,
            system_instruction=system_instruction,
        )
        print("\nSurvival Predictions (Batch):")
        for i, prediction in enumerate(batch_predictions):
            print(f"Report {i+1}: {prediction}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure to:")
        print("1. Have proper Google Cloud authentication set up")
        print("2. Have the required dependencies installed") 