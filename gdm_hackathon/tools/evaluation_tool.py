import importlib
import json
import gcsfs
from smolagents import tool
from gdm_hackathon.models.medgemma_query import get_survival_prediction_from_report_patient
import re
import pandas as pd

from gdm_hackathon.config import GCP_PROJECT_ID

SYSTEM_INSTRUCTION = (
    "You are a highly skilled biomedical researcher with extensive expertise in "
    "analyzing various types of medical data, including H&E stained images, bulk "
    "RNA sequencing, spatial transcriptomics, and comprehensive clinical and treatment "
    "records. Your primary task is to predict patient survival based on provided "
    "medical reports."
)

@tool
def evaluate_report_relevance_in_zero_shot(tool1_name: str, tool2_name: str) -> str:
    """
    Evaluate the relevance of a function designed to extract prognostic information from 
    various feature-specific reports (e.g. histopathological immune infiltration, or
    the spatial heterogeneity of TP53) into a unified patient-level report. The 
    evaluation is based on the ability of MedGemma to predict long vs short patient 
    survival from the unified report.
    
    Args:
        tool1_name (str): The name of the first sub report to be generated per patient
        tool2_name (str): The name of the second sub report to be generated per patient
        
    Returns:
        str: Accuracy score and evaluation details
    """
    
    # Load ground truth data
    fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
    bucket_name = "gdm-hackathon"
    ground_truth_path = f"gs://{bucket_name}/data/binary_os_mw_bladder.json"
    with fs.open(ground_truth_path, 'r') as f:
        ground_truth = json.load(f)
    
    correct_predictions = 0
    total_predictions = 0
    results = {}
    
    # import the tools function from the report_functions.py file using their names
    tool1_fn = getattr(importlib.import_module("gdm_hackathon.tools"), tool1_name)
    tool2_fn = getattr(importlib.import_module("gdm_hackathon.tools"), tool2_name)

    # Generate one report for all patients
    patient_names = list(ground_truth.keys())
    
    report = ""
    report += "--------------------------------\n"
    for patient_name in patient_names:
        report += f"""Patient report for {patient_name}:

{tool1_name} for {patient_name}:
{tool1_fn(patient_name)}

{tool2_name} for {patient_name}:
{tool2_fn(patient_name)}

--------------------------------\n"""

    report += f"""
Based on the above patient reports, predict for each patient whether they will have a long or short survival time.
There should be roughly the same number of long and short survival predictions.

Provide your answer in JSON format with two fields for each patient:
- "prediction": either "long survival" or "short survival"
- "reasoning": a brief explanation (keep it short, max 2-3 sentences)

```json
{{
"""
    for patient_name in patient_names:
        report += f"""
  "{patient_name}": {{
    "prediction": "long survival or short survival",
    "reasoning": "brief explanation"
  }}
"""
    report += """
}}
```
"""
        
    # Get batch predictions from MedGemma
    try:
        prediction_response = get_survival_prediction_from_report_patient(
            medical_report=report,
            system_instruction=SYSTEM_INSTRUCTION,
            max_tokens=4_096,
            temperature=0.0,
        )
        # Extract the prediction from the response
        prediction_text = prediction_response.strip()
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', prediction_text, re.DOTALL)
        # Process predictions
        results = json.loads(json_match.group(1))
        total_predictions = len(results)
    except Exception as e:
        # If batch fails, fall back to individual processing
        for patient_name in patient_names:
            results[patient_name] = {
                'error': f"Batch processing failed: {str(e)}",
                'ground_truth': ground_truth[patient_name]
            }
            total_predictions += 1
    
    # Calculate confusion matrix statistics
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    
    # Store examples for each category
    tp_examples = []
    fp_examples = []
    tn_examples = []
    fn_examples = []
    
    for patient in patient_names:
        if patient not in results:
            continue
        prediction = results[patient]['prediction']
        if prediction == 'long survival' and ground_truth[patient] == 1:
            true_positives += 1
            tp_examples.append((patient, results[patient]))
        elif prediction == 'long survival' and ground_truth[patient] == 0:
            false_positives += 1
            fp_examples.append((patient, results[patient]))
        elif prediction == 'short survival' and ground_truth[patient] == 0:
            true_negatives += 1
            tn_examples.append((patient, results[patient]))
        elif prediction == 'short survival' and ground_truth[patient] == 1:
            false_negatives += 1
            fn_examples.append((patient, results[patient]))
    
    # Calculate metrics
    correct_predictions = true_positives + true_negatives
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    precision = (true_positives / (true_positives + false_positives)) * 100 if (true_positives + false_positives) > 0 else 0
    recall = (true_positives / (true_positives + false_negatives)) * 100 if (true_positives + false_negatives) > 0 else 0
    specificity = (true_negatives / (true_negatives + false_positives)) * 100 if (true_negatives + false_positives) > 0 else 0
    
    # Format results
    result_summary = f"""
    Evaluation Results:
    - Total patients: {total_predictions}
    - Correct predictions: {correct_predictions}
    - Accuracy: {accuracy:.2f}%
    
    Confusion Matrix Statistics:
    - True Positives (TP): {true_positives}
    - False Positives (FP): {false_positives}
    - True Negatives (TN): {true_negatives}
    - False Negatives (FN): {false_negatives}
    
    Performance Metrics:
    - Precision: {precision:.2f}%
    - Recall (Sensitivity): {recall:.2f}%
    - Specificity: {specificity:.2f}%
    
    Example Cases with associated reasoning:
    """
    
    import random
    
    # Show random example from each category if available
    if tp_examples:
        patient, result = random.choice(tp_examples)
        result_summary += f"\nTrue Positive Example:"
        result_summary += f"\n  Predicted: long survival, Actual: long survival ✓"
        result_summary += f"\n  Reasoning: {result['reasoning']}\n"
    else:
        result_summary += "\nTrue Positive Example: No patients in this category\n"
    
    if fp_examples:
        patient, result = random.choice(fp_examples)
        result_summary += f"\nFalse Positive Example:"
        result_summary += f"\n  Predicted: long survival, Actual: short survival ✗"
        result_summary += f"\n  Reasoning: {result['reasoning']}\n"
    else:
        result_summary += "\nFalse Positive Example: No patients in this category\n"
    
    if tn_examples:
        patient, result = random.choice(tn_examples)
        result_summary += f"\nTrue Negative Example:"
        result_summary += f"\n  Predicted: short survival, Actual: short survival ✓"
        result_summary += f"\n  Reasoning: {result['reasoning']}\n"
    else:
        result_summary += "\nTrue Negative Example: No patients in this category\n"
    
    if fn_examples:
        patient, result = random.choice(fn_examples)
        result_summary += f"\nFalse Negative Example:"
        result_summary += f"\n  Predicted: short survival, Actual: long survival ✗"
        result_summary += f"\n  Reasoning: {result['reasoning']}\n"
    else:
        result_summary += "\nFalse Negative Example: No patients in this category\n"
    
    return result_summary 