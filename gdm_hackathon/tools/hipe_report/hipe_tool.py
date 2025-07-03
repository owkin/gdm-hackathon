#!/usr/bin/env python3
"""
Simple HIPE Report Tool using smolagents

This tool loads HIPE report data from Google Storage bucket using the @tool decorator.
"""
# %%

import gcsfs
from smolagents import tool

from gdm_hackathon.config import GCP_PROJECT_ID

@tool
def load_hipe_report(patient_id: str) -> str:
    """
    Load HIPE report data from Google Storage bucket for a specific patient.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'TCGA-2F-A9KO-01Z-00-DX1')
        
    Returns:
        The content of the HIPE report as a string
        
    Example:
        >>> load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1")
        "Patient shows signs of..."
    """
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        
        # Construct the path to the HIPE report in the bucket
        # Format: gdm-hackathon/hipe_reports/TCGA_BLCA/TCGA-2F-A9KO-01Z-00-DX1.195576CF-B739-4BD9-B15B-4A70AE287D3E.txt
        bucket_name = "gdm-hackathon"
        
        # Search for files that start with the patient ID
        possible_directories = [
            f"{bucket_name}/hipe_reports/TCGA_BLCA/",
            f"{bucket_name}/hipe_reports/"
        ]
        
        # Find the first existing path
        report_path = None
        for directory in possible_directories:
            if fs.exists(directory):
                try:
                    # List files in the directory and find one that starts with patient_id
                    files = fs.ls(directory)
                    for file_path in files:
                        filename = file_path.split('/')[-1]
                        if filename.startswith(patient_id):
                            report_path = file_path
                            break
                    if report_path:
                        break
                except Exception:
                    continue
        
        if not report_path:
            return f"Error: HIPE report not found for patient {patient_id}. Searched in directories: {', '.join(possible_directories)}"
        
        # Read the HIPE report content
        with fs.open(report_path, 'r') as f:
            content = f.read()
            
        return f"HIPE Report for {patient_id}:\n\n{content}"
        
    except Exception as e:
        return f"Error loading HIPE report for patient {patient_id}: {str(e)}"


# %%
if __name__ == "__main__":
    print(load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1"))

# %%