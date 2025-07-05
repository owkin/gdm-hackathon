"""
This tool loads clinical report data from Google Storage bucket using the @tool decorator.
"""

#%%
import json
from smolagents import tool
from gdm_hackathon.utils import get_gcs_fs
from functools import lru_cache

# %%

@lru_cache(maxsize=1)
def get_all_clinical_reports() -> dict:
    """
    Load all clinical report data from Google Storage bucket.
    
    This function reads the clinical report data from the Google Storage bucket and returns it as a string.
    
    Returns:
        The content of the clinical report as a string
        
    Example:
        >>> get_all_clinical_reports()
        "Clinical data for all patients shows..."
    """
    fs = get_gcs_fs()
    bucket_name = "gdm-hackathon"
    path = f"{bucket_name}/data/clinical_mw_bladder.json"

    # read the file
    with fs.open(path, 'r') as f:
        content = f.read()
    return json.loads(content)


@tool
def load_clinical_report(patient_id: str) -> str:
    """
    Load clinical report data from Google Storage bucket for a specific patient.
    
    This report consolidates key clinical and treatment data for the patient, including 
    age, smoking status, histological subtype, cancer stage, current medications, and 
    radiotherapy history.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the clinical report as a string
        
    Example:
        >>> load_clinical_report("test_patient")
        "Clinical data for patient shows..."
    """
    all_clinical_reports = get_all_clinical_reports()
    if patient_id == "test_patient":
        patient_id = "MW_B_001"       
    return all_clinical_reports[patient_id]
# %%
