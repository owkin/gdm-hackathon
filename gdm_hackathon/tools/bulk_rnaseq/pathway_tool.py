#!/usr/bin/env python3
"""
Bulk RNAseq Pathway Report Tools using smolagents

This module provides individual tools for loading pathway descriptions for each pathway.
Each tool loads the corresponding pathway description from Google Storage bucket.
"""
# %%

import gcsfs
import json
from smolagents import tool
from gdm_hackathon.config import GCP_PROJECT_ID


@tool
def load_fgfr3_pathway_report(patient_id: str) -> str:
    """
    Load FGFR3 pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of FGFR3 pathway activity in the patient's bulk RNAseq data.
    The FGFR3 pathway is the defining pathway for the Luminal Papillary subtype of bladder cancer.
    High activity is linked to better prognosis in early stages but resistance to immunotherapy.
    It's the primary target for FGFR inhibitors (e.g., erdafitinib).
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the FGFR3 pathway report as a string
        
    Example:
        >>> load_fgfr3_pathway_report("test_patient")
        "FGFR3 pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "fgfr3")


@tool
def load_egfr_pathway_report(patient_id: str) -> str:
    """
    Load EGFR pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of EGFR pathway activity in the patient's bulk RNAseq data.
    The EGFR pathway represents another major receptor tyrosine kinase pathway. High EGFR signaling
    is associated with tumor proliferation and worse prognosis. It's a marker of the aggressive
    Basal/Squamous subtype and can be a resistance mechanism to other therapies.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the EGFR pathway report as a string
        
    Example:
        >>> load_egfr_pathway_report("test_patient")
        "EGFR pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "egfr")


@tool
def load_pi3k_pathway_report(patient_id: str) -> str:
    """
    Load PI3K pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of PI3K pathway activity in the patient's bulk RNAseq data.
    The PI3K/AKT pathway is a central pro-survival and pro-growth pathway downstream of many receptors.
    High activity is linked to cell survival, proliferation, and resistance to apoptosis. It's a marker
    of aggressive disease and a target for PI3K/AKT inhibitors. Co-activation with MAPK is a known resistance mechanism.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the PI3K pathway report as a string
        
    Example:
        >>> load_pi3k_pathway_report("test_patient")
        "PI3K pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "pi3k")


@tool
def load_anti_pd1_pathway_report(patient_id: str) -> str:
    """
    Load Anti-PD1 pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Anti-PD1 pathway activity in the patient's bulk RNAseq data.
    The Anti-PD-1 Response/IFN-γ signature is the canonical "hot tumor" signature measuring T-cell
    infiltration and interferon-gamma signaling. It's the strongest predictor of a positive response
    to immunotherapy and often associated with the aggressive but immunologically active Basal/Squamous subtype.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the Anti-PD1 pathway report as a string
        
    Example:
        >>> load_anti_pd1_pathway_report("test_patient")
        "Anti-PD1 pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "anti_pd1")


@tool
def load_tgf_beta_pathway_report(patient_id: str) -> str:
    """
    Load TGF-beta pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of TGF-beta pathway activity in the patient's bulk RNAseq data.
    The TGF-β pathway is a powerful immunosuppressive and pro-fibrotic pathway that creates a physical
    and chemical barrier preventing T-cells from infiltrating and attacking the tumor. High activity
    is a major mechanism of primary and acquired resistance to immunotherapy and is associated with
    an "immune-excluded" phenotype and poor prognosis.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the TGF-beta pathway report as a string
        
    Example:
        >>> load_tgf_beta_pathway_report("test_patient")
        "TGF-beta pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "tgf_beta")


@tool
def load_hypoxia_pathway_report(patient_id: str) -> str:
    """
    Load Hypoxia pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Hypoxia pathway activity in the patient's bulk RNAseq data.
    The Hypoxia pathway measures the cellular response to low oxygen, a common state in poorly
    vascularized tumors. It drives angiogenesis (new blood vessel formation) and is strongly
    associated with metastasis, therapy resistance, and poor prognosis. It often overlaps with the EMT signature.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the Hypoxia pathway report as a string
        
    Example:
        >>> load_hypoxia_pathway_report("test_patient")
        "Hypoxia pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "hypoxia")


@tool
def load_emt_pathway_report(patient_id: str) -> str:
    """
    Load EMT pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of EMT (Epithelial-Mesenchymal Transition) pathway activity
    in the patient's bulk RNAseq data. EMT is a shift from a stable, epithelial state to a mobile,
    invasive mesenchymal state. It's strongly associated with tumor invasion, metastasis, chemoresistance,
    and very poor prognosis. A hallmark of the most aggressive bladder cancers.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the EMT pathway report as a string
        
    Example:
        >>> load_emt_pathway_report("test_patient")
        "EMT pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "emt")


@tool
def load_cell_cycle_pathway_report(patient_id: str) -> str:
    """
    Load Cell Cycle pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of Cell Cycle pathway activity in the patient's bulk RNAseq data.
    The Cell Cycle pathway measures the rate of cell division (G2/M phase). High proliferation indicates
    an aggressive tumor and worse prognosis. It can predict sensitivity to traditional chemotherapy.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the Cell Cycle pathway report as a string
        
    Example:
        >>> load_cell_cycle_pathway_report("test_patient")
        "Cell Cycle pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "cell_cycle")


@tool
def load_ddr_deficiency_pathway_report(patient_id: str) -> str:
    """
    Load DDR (DNA Damage Response) Deficiency pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of DDR pathway activity in the patient's bulk RNAseq data.
    The DDR pathway measures defects in the cell's machinery for fixing DNA breaks. A high score
    indicates a tumor that cannot repair the damage caused by platinum-based chemotherapy and PARP inhibitors,
    predicting sensitivity to these treatments.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the DDR Deficiency pathway report as a string
        
    Example:
        >>> load_ddr_deficiency_pathway_report("test_patient")
        "DDR Deficiency pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "ddr_deficiency")


@tool
def load_p53_pathway_report(patient_id: str) -> str:
    """
    Load P53 pathway description from Google Storage bucket for a specific patient.
    
    This report describes the analysis of P53 pathway activity in the patient's bulk RNAseq data.
    The p53 pathway reflects the activity of TP53, the "guardian of the genome." In over 50% of MIBC,
    TP53 is mutated, leading to an inactivated pathway. p53 inactivation (a low activity score) is
    associated with genomic instability, resistance to apoptosis, and very poor prognosis. It's a hallmark
    of high-grade, aggressive disease.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the P53 pathway report as a string
        
    Example:
        >>> load_p53_pathway_report("test_patient")
        "P53 pathway analysis shows..."
    """
    return _load_pathway_description(patient_id, "p53")


def _load_pathway_description(patient_id: str, pathway_name: str) -> str:
    """
    Helper function to load pathway report from Google Storage bucket.
    
    Args:
        patient_id: The unique identifier for the patient
        pathway_name: The name of the pathway (fgfr3, egfr, pi3k, anti_pd1, tgf_beta, hypoxia, emt, cell_cycle, ddr_deficiency, p53)
        
    Returns:
        The content of the pathway report as a string
    """
    if patient_id == "test_patient":
        patient_id = "MW_B_001"
    if patient_id.endswith("a"):
        patient_id = patient_id[:-1]
        
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        bucket_name = "gdm-hackathon"
        
        # Construct the path to the pathway description
        description_path = f"{bucket_name}/data/bulk_rna_pathways/descriptions/{patient_id}_{pathway_name}_description.json"
        
        # Check if the description exists
        if not fs.exists(description_path):
            return f"Error: Pathway description not found for patient {patient_id} and pathway {pathway_name}. Path: {description_path}"
        
        # Read the pathway description content
        with fs.open(description_path, 'r') as f:
            data = json.load(f)
            
        # Extract the summary from the JSON data
        summary = data.get("summary", "No summary found in the file")
        pathway_score = data.get("pathway_score", "N/A")
        
        return f"Pathway Analysis for {patient_id} - {pathway_name.upper()} (Score: {pathway_score}):\n\n{summary}"
        
    except Exception as e:
        return f"Error loading pathway description for patient {patient_id} and pathway {pathway_name}: {str(e)}"


# %%
if __name__ == "__main__":
    # Test one of the tools
    print(load_fgfr3_pathway_report("test_patient"))

# %% 