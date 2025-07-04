import json
from smolagents import tool
from pathlib import Path

CACHE_FOLDER = Path("/Users/apignet/Documents/Codebase/gdm-hackathon/gdm_hackathon/poc/precomputed_folder")

@tool
def get_clinical_report(patient_name: str) -> str:
    """Get clinical report for a specific patient.
    
    This report contains comprehensive clinical information including patient demographics,
    cancer diagnosis with staging, performance status, comorbidities, and treatment plans.
    
    Args:
        patient_name (str): The name of the patient to get the clinical report for.
        
    Returns:
        str: The clinical report containing patient demographics, cancer diagnosis,
             TNM staging, ECOG performance status, comorbidities, and treatment plan.
    """
    with open(CACHE_FOLDER / 'clinical.json', 'r') as f:
        data = json.load(f)
    report =data.get(patient_name, "Patient not found")

    if report == "Patient not found":
        return _the_tool_but_not_cached(patient_name)

@tool
def get_hipe_report(patient_name: str) -> str:
    """Get histology biomarker (HIPE) report for a specific patient.
    
    This report contains comprehensive immune infiltration analysis including immune cell
    composition, spatial distribution, tumor-immune interactions, and microenvironment
    characteristics based on whole slide image analysis.
    
    Args:
        patient_name (str): The name of the patient to get the HIPE report for.
        
    Returns:
        str: The histology biomarker report with detailed immune infiltration analysis,
             including cell counts, densities, spatial relationships, and biological
             interpretation of the tumor microenvironment.
    """
    with open(CACHE_FOLDER / 'hipe_report.json', 'r') as f:
        data = json.load(f)
    return data.get(patient_name, "Patient not found")

@tool
def get_spt_report(patient_name: str) -> str:
    """Get spatial transcriptomics (SPT) report for a specific patient.
    
    This report contains information about the most expressed genes in tumor regions
    and surrounding tissue, including transcript counts and biological interpretations.
    
    Args:
        patient_name (str): The name of the patient to get the SPT report for.
        
    Returns:
        str: The spatial transcriptomics report with gene expression data for tumor
             and non-tumor regions, including transcript counts and biological context.
    """
    with open(CACHE_FOLDER / 'spt_report.json', 'r') as f:
        data = json.load(f)
    return data.get(patient_name, "Patient not found") 