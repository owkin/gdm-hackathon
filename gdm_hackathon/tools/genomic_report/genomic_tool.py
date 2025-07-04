#!/usr/bin/env python3
"""
Genomic Report Tools using smolagents

This module provides individual tools for loading genomic descriptions for each data type.
Each tool loads the corresponding genomic description from Google Storage bucket.
"""
# %%

import gcsfs
import json
from smolagents import tool
from gdm_hackathon.config import GCP_PROJECT_ID


@tool
def load_snv_indel_genomic_report(patient_id: str) -> str:
    """
    Load SNV/INDEL genomic description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Single Nucleotide Variants (SNVs) and Insertions/Deletions (INDELs)
    in the patient's genomic data. SNVs and INDELs are the most common types of genetic variations
    and can have significant implications for disease development, progression, and treatment response.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the SNV/INDEL genomic report as a string
        
    Example:
        >>> load_snv_indel_genomic_report("test_patient")
        "SNV/INDEL analysis shows..."
    """
    return _load_genomic_description(patient_id, "snv_indel")


@tool
def load_cnv_genomic_report(patient_id: str) -> str:
    """
    Load CNV genomic description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Copy Number Variations (CNVs) in the patient's genomic data.
    CNVs are structural variations where the number of copies of a particular gene or genomic region
    differs from the reference genome. These variations can significantly impact gene expression
    and are important in cancer development and progression.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the CNV genomic report as a string
        
    Example:
        >>> load_cnv_genomic_report("test_patient")
        "CNV analysis shows..."
    """
    return _load_genomic_description(patient_id, "cnv")


@tool
def load_cna_genomic_report(patient_id: str) -> str:
    """
    Load CNA genomic description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Copy Number Alterations (CNAs) in the patient's genomic data.
    CNAs include both amplifications (increased copy number) and deletions (decreased copy number)
    of genomic regions. These alterations are common in cancer and can affect tumor behavior,
    prognosis, and response to targeted therapies.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the CNA genomic report as a string
        
    Example:
        >>> load_cna_genomic_report("test_patient")
        "CNA analysis shows..."
    """
    return _load_genomic_description(patient_id, "cna")


@tool
def load_gii_genomic_report(patient_id: str) -> str:
    """
    Load GII genomic description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of the Genomic Instability Index (GII) for the patient.
    GII is a measure of genomic instability that quantifies the extent of chromosomal aberrations
    and structural variations in the genome. High GII values are associated with increased
    genomic instability, which is a hallmark of cancer and can indicate aggressive disease.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the GII genomic report as a string
        
    Example:
        >>> load_gii_genomic_report("test_patient")
        "GII analysis shows..."
    """
    return _load_genomic_description(patient_id, "gii")


@tool
def load_tmb_genomic_report(patient_id: str) -> str:
    """
    Load TMB genomic description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Tumor Mutational Burden (TMB) for the patient.
    TMB measures the total number of mutations per megabase of DNA in a tumor sample.
    High TMB is associated with increased neoantigen production and can predict response
    to immunotherapy, particularly immune checkpoint inhibitors.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the TMB genomic report as a string
        
    Example:
        >>> load_tmb_genomic_report("test_patient")
        "TMB analysis shows..."
    """
    return _load_genomic_description(patient_id, "tmb")


def _load_genomic_description(patient_id: str, data_type: str) -> str:
    """
    Helper function to load genomic report from Google Storage bucket.
    
    Args:
        patient_id: The unique identifier for the patient
        data_type: The type of genomic data (snv_indel, cnv, cna, gii, tmb)
        
    Returns:
        The content of the genomic report as a string
    """
    if patient_id == "test_patient":
        patient_id = "MW_B_001a"
        
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        bucket_name = "gdm-hackathon"
        
        # Construct the path to the genomic description
        description_path = f"{bucket_name}/data/mutated_genes/descriptions/{patient_id}_{data_type}_description.json"
        
        # Check if the description exists
        if not fs.exists(description_path):
            return f"Error: Genomic description not found for patient {patient_id} and data type {data_type}. Path: {description_path}"
        
        # Read the genomic description content
        with fs.open(description_path, 'r') as f:
            data = json.load(f)
            
        # Extract the summary from the JSON data
        summary = data.get("summary", "No summary found in the file")
        
        return f"Genomic Analysis for {patient_id} - {data_type.upper()}:\n\n{summary}"
        
    except Exception as e:
        return f"Error loading genomic description for patient {patient_id} and data type {data_type}: {str(e)}"


# %%
if __name__ == "__main__":
    # Test one of the tools
    print(load_snv_indel_genomic_report("test_patient"))

# %% 