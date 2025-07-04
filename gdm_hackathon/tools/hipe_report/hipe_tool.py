#!/usr/bin/env python3
"""
Simple HIPE Report Tool using smolagents

This tool loads HIPE report data from Google Storage bucket using the @tool decorator.
"""
# %%

from functools import lru_cache
from typing import Optional
import gcsfs
from smolagents import tool

from gdm_hackathon.config import GCP_PROJECT_ID


@lru_cache(maxsize=1)
def _get_gcs_fs():
    # Initialize GCS filesystem
    return gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)


def _find_report(subdirectory: str, patient_id: str) -> Optional[str]:
    fs = _get_gcs_fs()
    
    if patient_id == "test_patient":
        patient_id = "MW_B_007"
        
    # Construct the path to the HIPE report in the bucket
    bucket_name = "gdm-hackathon"

    directory = f"{bucket_name}/data/{subdirectory}/"

    if not fs.exists(directory):
        return None

    try:
        # List files in the directory and find one that starts with patient_id
        files = fs.ls(directory)
        for file_path in files:
            filename = file_path.split('/')[-1]
            if filename.startswith(patient_id):
                return file_path
    except Exception as exc:
        return None

    return None


@tool
def load_histopathological_immune_infiltration_report(patient_id: str) -> str:
    """
    Load a histopathological report describing the immune infiltration of the tumor.

    The report describes the immune cell densities, the spatial organization of the
    immune cells (plasmocytes, neutrophils, eosinophils, lymphocytes).

    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')

    Returns:
        The content of the immune infiltration report as a string

    Example:
        >>> get_hipe_report("test_patient")
        "Patient shows signs of..."
    """
    fs = _get_gcs_fs()

    try:
        report_path = _find_report("hipe_reports_immune_mw", patient_id)

        if not report_path:
            return f"Error: HIPE immune infiltration report not found for patient {patient_id}."

        # Read the HIPE report content
        with fs.open(report_path, 'r') as f:
            content = f.read()

        return f"Histopathological assessment of the tumor immune infiltration for {patient_id}:\n\n{content}"

    except Exception as e:
        return f"Error loading immune infiltration report for patient {patient_id}: {str(e)}"


@tool
def load_histopathological_tumor_stroma_compartments_report(patient_id: str) -> str:
    """
    Load a histopathological report assessing the organization of the tumor-stroma compartments.

    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')

    Returns:
        The content of the tumor-stroma compartment report as a string

    Example:
        >>> load_hipe_report("test_patient")
        "Patient shows signs of..."
    """
    fs = _get_gcs_fs()

    try:
        report_path = _find_report("hipe_reports_tumor_stroma_compartments_mw", patient_id)

        if not report_path:
            return f"Error: HIPE tumor stroma compartment report not found for patient {patient_id}."

        # Read the HIPE report content
        with fs.open(report_path, 'r') as f:
            content = f.read()

        return f"Histopathological assessment of the tumor stroma compartments for {patient_id}:\n\n{content}"

    except Exception as e:
        return f"Error loading tumor-stroma compartment report for patient {patient_id}: {str(e)}"


@tool
def load_histopathological_tumor_nuclear_morphometry_report(patient_id: str) -> str:
    """
    Load a histopathological report assessing the tumor nuclear morphometry.

    Args:
        patient_id: The unique identifier for the patient (e.g., 'TCGA-2F-A9KO-01Z-00-DX1')

    Returns:
        The content of the tumor nuclear morphometry report as a string

    Example:
        >>> load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1")
        "Patient shows signs of..."
    """
    fs = _get_gcs_fs()

    try:
        report_path = _find_report("hipe_reports_nuclear_morphometry_mw", patient_id)

        if not report_path:
            return f"Error: HIPE tumor nuclear morphometry report not found for patient {patient_id}."

        # Read the HIPE report content
        with fs.open(report_path, 'r') as f:
            content = f.read()

        return f"Histopathological assessment of the tumor nuclear morphometry for {patient_id}:\n\n{content}"

    except Exception as e:
        return f"Error loading tumor nuclear morphometry report for patient {patient_id}: {str(e)}"


# %%
if __name__ == "__main__":
    print(load_histopathological_immune_infiltration_report("test_patient"))
    print(load_histopathological_tumor_stroma_compartments_report("test_patient"))
    print(load_histopathological_tumor_nuclear_morphometry_report("test_patient"))

# %%