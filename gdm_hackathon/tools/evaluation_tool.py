
# %% 
import importlib
import json
import gcsfs
import re
import random
from smolagents import tool
from gdm_hackathon.models.medgemma_query import get_survival_prediction_batch
from gdm_hackathon.config import GCP_PROJECT_ID

# %%

SYSTEM_INSTRUCTION = (
    "You are a highly skilled biomedical researcher. Your task is to predict relative "
    "patient survival. You will be given a summary of a patient cohort, followed by "
    "a specific patient's data. Your prediction for the individual must be based on "
    "comparing their data to the provided cohort context."
)

def get_cohort_summary(tool_name: str, reports_dict: dict, patient_names: list) -> str:
    """
    Uses an LLM to generate a summary for a specific feature across the entire cohort.
    """
    print(f"Generating cohort summary for: {tool_name}...")
    
    # Combine all individual reports into one text block
    all_reports_text = "\n---\n".join([reports_dict[p] for p in patient_names])
    
    summary_prompt = f"""
    The following are {len(patient_names)} individual medical reports about '{tool_name}'.
    Summarize the key findings for the entire cohort. Focus on the range of observations 
    (e.g., high vs. low values), any central tendency, and the overall clinical picture 
    for this specific feature. Keep the summary to 6-8 sentences.
    ---
    REPORTS:
    {all_reports_text}
    ---
    COHORT SUMMARY:
    """
    
    try:
        # We use the batch prediction function with a single prompt for simplicity
        summary_response = get_survival_prediction_batch(
            medical_reports=[summary_prompt],
            system_instruction="You are a helpful medical data summarizer.",
            max_tokens=1000,
            temperature=0.2,
        )
        # Extract the text from the response
        summary_text = summary_response[0].strip()
        # Clean up potential JSON formatting from the response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', summary_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)).get('reasoning', summary_text)
        return summary_text

    except Exception as e:
        print(f"Could not generate cohort summary for {tool_name}: {e}")
        return f"Summary generation failed for {tool_name}."

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
    fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
    ground_truth_path = "gs://gdm-hackathon/data/binary_os_mw_bladder.json"
    with fs.open(ground_truth_path, 'r') as f:
        ground_truth = json.load(f)
        
    patient_names = list(ground_truth.keys())
    
    # --- 1. Generate All Reports Upfront ---
    print("Generating individual reports for all patients...")
    tool1_fn = getattr(importlib.import_module("gdm_hackathon.tools"), tool1_name)
    tool2_fn = getattr(importlib.import_module("gdm_hackathon.tools"), tool2_name)
    
    all_reports_t1 = {p_name: tool1_fn(p_name) for p_name in patient_names}
    all_reports_t2 = {p_name: tool2_fn(p_name) for p_name in patient_names}

    # --- 2. Create Cohort Summaries ---
    cohort_summary_t1 = get_cohort_summary(tool1_name, all_reports_t1, patient_names)
    cohort_summary_t2 = get_cohort_summary(tool2_name, all_reports_t2, patient_names)

    # --- 3. Build Context-Aware Prompts for Each Patient ---
    patient_prompts = []
    for patient_name in patient_names:
        prompt = f"""
You are a biomedical researcher making a comparative survival prediction.

## Cohort-Level Context
First, here are the summary characteristics for the entire patient cohort for the two features under consideration:

### Cohort Summary for Feature 1 ({tool1_name}):
{cohort_summary_t1}

### Cohort Summary for Feature 2 ({tool2_name}):
{cohort_summary_t2}

---

## Individual Patient Analysis
Now, analyze the following specific patient in the context of the cohort summaries above.

### Patient Report for: {patient_name}
- **Feature 1 ({tool1_name})**: {all_reports_t1[patient_name]}
- **Feature 2 ({tool2_name})**: {all_reports_t2[patient_name]}

---

## Prediction Task
Based on the individual patient's report **in comparison to the cohort context**, predict whether this patient will belong to the upper 50% (long survival) or the lower 50% (short survival) of the survival distribution.
Hint: there is roughly a 50% chance of long survival and 50% chance of short survival. 

Very important ! Provide your answer in JSON format with two fields:
- "prediction": either "long survival" or "short survival"
- "reasoning": a brief explanation of how the patient compares to the cohort (max 2-3 sentences)

```json
{{
  "prediction": "long survival" or "short survival",
  "reasoning": "brief explanation"
}}
```

For example:
```json
{{
  "prediction": "long survival",
  "reasoning": "The patient has a high CDK12 expression and a low DC expression, which is associated with long survival."
}}
```

or 
```json
{{
  "prediction": "short survival",
  "reasoning": "The patient has a low CDK12 expression and a high DC expression, which is associated with short survival."
}}
```

Let's predict! 
"""
        patient_prompts.append(prompt)
    
    # Get batch predictions from MedGemma
    batch_predictions = get_survival_prediction_batch(
        medical_reports=patient_prompts,
        system_instruction=SYSTEM_INSTRUCTION,
        max_tokens=2_000,
        temperature=0.0,
    )
    results = {}
    parsed_predictions = 0
    correct_predictions =0
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
                    
                    if 'long survival' in prediction_field:
                        prediction = 1
                    elif 'short survival' in prediction_field:
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
                if 'long survival' in answer_content:
                    prediction = 1
                elif 'short survival' in answer_content:
                    prediction = 0
                else:
                    # Fallback: try to find any indication of response
                    if any(word in answer_content for word in ['good', 'positive', 'survival', 'success']):
                        prediction = 1
                    elif any(word in answer_content for word in ['bad', 'negative', 'fail', 'poor', 'death']):
                        prediction = 0
                    else:
                        raise ValueError(f"Could not parse response: {answer_content}")
            
            # Compare with ground truth
            true_value = ground_truth[patient_name]
            is_correct = prediction == true_value
            
            if is_correct:
                correct_predictions += 1
                        
            results[patient_name] = {
                'prediction': prediction,
                'ground_truth': true_value,
                'correct': is_correct,
                'raw_response': prediction_text,
                'reasoning': reasoning if 'reasoning' in locals() else 'No reasoning provided'
            }
            parsed_predictions += 1
            
        except Exception as e:
            results[patient_name] = {
                'error': f"Failed to parse prediction: {str(e)}",
                'ground_truth': ground_truth[patient_name],
                'raw_response': prediction_response
            }
            
                
    
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
    
    total_predictions = len(patient_names)

    for patient, result in results.items():
        if 'error' not in result:
            prediction = result['prediction']
            ground_truth = result['ground_truth']
            
            if prediction == 1 and ground_truth == 1:
                true_positives += 1
                tp_examples.append((patient, result))
            elif prediction == 1 and ground_truth == 0:
                false_positives += 1
                fp_examples.append((patient, result))
            elif prediction == 0 and ground_truth == 0:
                true_negatives += 1
                tn_examples.append((patient, result))
            elif prediction == 0 and ground_truth == 1:
                false_negatives += 1
                fn_examples.append((patient, result))
    
    # Calculate metrics
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    precision = (true_positives / (true_positives + false_positives)) * 100 if (true_positives + false_positives) > 0 else 0
    recall = (true_positives / (true_positives + false_negatives)) * 100 if (true_positives + false_negatives) > 0 else 0
    specificity = (true_negatives / (true_negatives + false_positives)) * 100 if (true_negatives + false_positives) > 0 else 0
    
    # Format results
    result_summary = f"""
    Evaluation Results:
    - Total patients: {total_predictions}
    - Correct predictions: {correct_predictions}
    - Parsed predictions: {parsed_predictions}
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
    
    # Show random example from each category if available
    if tp_examples:
        patient, result = random.choice(tp_examples)
        result_summary += f"\nTrue Positive Example:"
        result_summary += f"\n  Predicted: long survival, Actual: long survival ✓"
        result_summary += f"\n  Reasoning: {result.get('reasoning', 'No reasoning provided')}\n"
    else:
        result_summary += "\nTrue Positive Example: No patients in this category\n"
    
    if fp_examples:
        patient, result = random.choice(fp_examples)
        result_summary += f"\nFalse Positive Example:"
        result_summary += f"\n  Predicted: long survival, Actual: short survival ✗"
        result_summary += f"\n  Reasoning: {result.get('reasoning', 'No reasoning provided')}\n"
    else:
        result_summary += "\nFalse Positive Example: No patients in this category\n"
    
    if tn_examples:
        patient, result = random.choice(tn_examples)
        result_summary += f"\nTrue Negative Example:"
        result_summary += f"\n  Predicted: short survival, Actual: short survival ✓"
        result_summary += f"\n  Reasoning: {result.get('reasoning', 'No reasoning provided')}\n"
    else:
        result_summary += "\nTrue Negative Example: No patients in this category\n"
    
    if fn_examples:
        patient, result = random.choice(fn_examples)
        result_summary += f"\nFalse Negative Example:"
        result_summary += f"\n  Predicted: short survival, Actual: long survival ✗"
        result_summary += f"\n  Reasoning: {result.get('reasoning', 'No reasoning provided')}\n"
    else:
        result_summary += "\nFalse Negative Example: No patients in this category\n"
    
    return result_summary 



if __name__ == "__main__":
    tool1_name = "load_histopathological_tumor_stroma_compartments_report"
    tool2_name = "load_clinical_report"
    print(evaluate_report_relevance_in_zero_shot(tool1_name, tool2_name))
# %%
