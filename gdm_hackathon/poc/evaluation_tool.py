import importlib
import json
from smolagents import tool
from gdm_hackathon.models.medgemma_query import get_survival_prediction_batch
import re

from gdm_hackathon.models.vertex_models import MODELS_DICT, LOCATION
from gdm_hackathon.poc.report_functions import CACHE_FOLDER


@tool
def evaluate_report_relevance_in_zero_shot(tool1_name: str, tool2_name: str) -> str:
    """
    Evaluate the relevance of a report generation function by predicting treatment response
    using MedGemma and comparing to ground truth.
    
    Args:
        tool1_name (str): The name of the first sub report to be generated per patient
        tool2_name (str): The name of the second sub report to be generated per patient
        
    Returns:
        str: Accuracy score and evaluation details
    """
    
    # Load ground truth data
    with open(CACHE_FOLDER / 'response_to_treatment.json', 'r') as f:
        ground_truth = json.load(f)
    
    # MedGemma endpoint configuration
    ENDPOINT_ID = MODELS_DICT["medgemma-27b"]['endpoint_id']
    
    
    correct_predictions = 0
    total_predictions = 0
    results = {}
    
    # import the tools function from the report_functions.py file using their names
    tool1_fn = getattr(importlib.import_module("gdm_hackathon.poc.report_functions"), tool1_name)
    tool2_fn = getattr(importlib.import_module("gdm_hackathon.poc.report_functions"), tool2_name)

    # Generate reports for all patients
    patient_reports = []
    patient_names = list(ground_truth.keys())
    
    for patient_name in patient_names:
        report = f"""Patient report for {patient_name}:

{tool1_fn(patient_name)}

{tool2_fn(patient_name)}

Based on the above patient report, determine if this patient was a good responder or bad responder to treatment.

Provide your answer in JSON format with two fields:
- "prediction": either "good responder" or "bad responder"
- "reasoning": a brief explanation (keep it short, max 2-3 sentences)

```json
{{
  "prediction": "good responder or bad responder",
  "reasoning": "brief explanation"
}}
```
"""
        
        patient_reports.append(report)
    
    # Get batch predictions from MedGemma
    try:
        batch_predictions = get_survival_prediction_batch(
            medical_reports=patient_reports,
            endpoint_id=ENDPOINT_ID,
            endpoint_region=LOCATION,
            max_tokens=2_000,
            temperature=0.0
        )
        
        # Process predictions
        for i, (patient_name, prediction_response) in enumerate(zip(patient_names, batch_predictions)):
            try:
                # Extract the prediction from the response
                prediction_text = prediction_response['predictions'][0].strip()
                
                
                # Look for JSON content in the response
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', prediction_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    try:
                        parsed_response = json.loads(json_str)
                        prediction_field = parsed_response.get('prediction', '').lower()
                        reasoning = parsed_response.get('reasoning', '')
                        
                        if 'good responder' in prediction_field:
                            prediction = 1
                        elif 'bad responder' in prediction_field:
                            prediction = 0
                        else:
                            raise ValueError(f"Invalid prediction value: {prediction_field}")
                            
                    except json.JSONDecodeError:
                        raise ValueError(f"Failed to parse JSON: {json_str}")
                else:
                    # Fallback: look for the answer within <answer> tags
                    answer_match = re.search(r'<answer>(.*?)</answer>', prediction_text, re.DOTALL)
                    if answer_match:
                        answer_content = answer_match.group(1).strip().lower()
                    else:
                        # Fallback: use the whole response
                        answer_content = prediction_text.strip().lower()
                    
                    # Parse the response
                    if 'good responder' in answer_content:
                        prediction = 1
                    elif 'bad responder' in answer_content:
                        prediction = 0
                    else:
                        # Fallback: try to find any indication of response
                        if any(word in answer_content for word in ['good', 'positive', 'respond', 'success']):
                            prediction = 1
                        elif any(word in answer_content for word in ['bad', 'negative', 'fail', 'poor']):
                            prediction = 0
                        else:
                            raise ValueError(f"Could not parse response: {answer_content}")
                
                # Compare with ground truth
                true_value = ground_truth[patient_name]
                is_correct = prediction == true_value
                
                if is_correct:
                    correct_predictions += 1
                
                total_predictions += 1
                
                results[patient_name] = {
                    'prediction': prediction,
                    'ground_truth': true_value,
                    'correct': is_correct,
                    'raw_response': prediction_text,
                    'reasoning': reasoning if 'reasoning' in locals() else 'No reasoning provided'
                }
                
            except Exception as e:
                results[patient_name] = {
                    'error': f"Failed to parse prediction: {str(e)}",
                    'ground_truth': ground_truth[patient_name],
                    'raw_response': prediction_response
                }
                total_predictions += 1
                
    except Exception as e:
        # If batch fails, fall back to individual processing
        for patient_name in patient_names:
            results[patient_name] = {
                'error': f"Batch processing failed: {str(e)}",
                'ground_truth': ground_truth[patient_name]
            }
            total_predictions += 1
    
    # Calculate accuracy
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    
    # Format results
    result_summary = f"""
    Evaluation Results:
    - Total patients: {total_predictions}
    - Correct predictions: {correct_predictions}
    - Accuracy: {accuracy:.2f}%
    
    Detailed Results:
    """
    
    for patient, result in results.items():
        if 'error' in result:
            result_summary += f"\n{patient}: Error - {result['error']}"
        else:
            result_summary += f"\n{patient}: Predicted {result['prediction']}, Actual {result['ground_truth']}, {'✓' if result['correct'] else '✗'}"
    
    return result_summary 