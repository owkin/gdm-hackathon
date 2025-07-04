#!/usr/bin/env python3
"""
Heatmap Report Tools using smolagents

This module provides individual tools for loading heatmap descriptions for each feature.
Each tool loads the corresponding heatmap description from Google Storage bucket.
"""
# %%

import gcsfs
import json
from smolagents import tool
from gdm_hackathon.config import GCP_PROJECT_ID
from gdm_hackathon.utils import convert_to_ch_id


@tool
def load_b_cell_heatmap_report(patient_id: str) -> str:
    """
    Load B cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of B cells (B lymphocytes) 
    in the tissue sample. B cells are part of the adaptive immune system and play a 
    crucial role in antibody production and immune memory.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the B cell heatmap report as a string
        
    Example:
        >>> load_b_cell_heatmap_report("test_patient")
        "B cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "B_cell")


@tool
def load_cdk12_heatmap_report(patient_id: str) -> str:
    """
    Load CDK12 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of CDK12 gene expression levels in the tissue sample.
    CDK12 is a cyclin-dependent kinase involved in transcription regulation and DNA damage response.
    High expression may indicate active transcription processes or DNA repair mechanisms.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the CDK12 heatmap report as a string
        
    Example:
        >>> load_cdk12_heatmap_report("test_patient")
        "CDK12 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "CDK12")


@tool
def load_dc_heatmap_report(patient_id: str) -> str:
    """
    Load dendritic cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of dendritic cells in the tissue sample.
    Dendritic cells are antigen-presenting cells that bridge innate and adaptive immunity.
    Their distribution patterns can indicate immune activation and antigen processing sites.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the dendritic cell heatmap report as a string
        
    Example:
        >>> load_dc_heatmap_report("test_patient")
        "Dendritic cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "DC")


@tool
def load_egfr_heatmap_report(patient_id: str) -> str:
    """
    Load EGFR gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of EGFR (Epidermal Growth Factor Receptor) 
    gene expression levels in the tissue sample. EGFR is a key receptor tyrosine kinase 
    involved in cell proliferation, survival, and differentiation. Overexpression is 
    associated with various cancers and can indicate aggressive tumor behavior.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the EGFR heatmap report as a string
        
    Example:
        >>> load_egfr_heatmap_report("test_patient")
        "EGFR expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "EGFR")


@tool
def load_erbb2_heatmap_report(patient_id: str) -> str:
    """
    Load ERBB2 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of ERBB2 (HER2) gene expression levels 
    in the tissue sample. ERBB2 is a receptor tyrosine kinase that regulates cell growth 
    and differentiation. Amplification and overexpression are important prognostic and 
    predictive markers in several cancer types.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the ERBB2 heatmap report as a string
        
    Example:
        >>> load_erbb2_heatmap_report("test_patient")
        "ERBB2 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "ERBB2")


@tool
def load_endothelial_heatmap_report(patient_id: str) -> str:
    """
    Load endothelial cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of endothelial cells in the tissue sample.
    Endothelial cells line blood vessels and play crucial roles in angiogenesis, 
    vascular permeability, and immune cell trafficking. Their distribution can indicate 
    vascular density and potential areas of active angiogenesis.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the endothelial cell heatmap report as a string
        
    Example:
        >>> load_endothelial_heatmap_report("test_patient")
        "Endothelial cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Endothelial")


@tool
def load_epithelial_heatmap_report(patient_id: str) -> str:
    """
    Load epithelial cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of epithelial cells in the tissue sample.
    Epithelial cells form the lining of organs and tissues and are often the origin of carcinomas.
    Their distribution patterns can indicate tissue architecture and potential areas of 
    epithelial-mesenchymal transition or tumor formation.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the epithelial cell heatmap report as a string
        
    Example:
        >>> load_epithelial_heatmap_report("test_patient")
        "Epithelial cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Epithelial")


@tool
def load_fgfr3_heatmap_report(patient_id: str) -> str:
    """
    Load FGFR3 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of FGFR3 (Fibroblast Growth Factor Receptor 3) 
    gene expression levels in the tissue sample. FGFR3 is involved in cell proliferation, 
    differentiation, and survival. Mutations and overexpression are associated with 
    various cancers including bladder cancer.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the FGFR3 heatmap report as a string
        
    Example:
        >>> load_fgfr3_heatmap_report("test_patient")
        "FGFR3 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "FGFR3")


@tool
def load_fibroblast_heatmap_report(patient_id: str) -> str:
    """
    Load fibroblast heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of fibroblasts in the tissue sample.
    Fibroblasts are the main cell type of connective tissue and play crucial roles in 
    extracellular matrix production, tissue repair, and cancer-associated fibroblast 
    functions. Their distribution can indicate areas of tissue remodeling and fibrosis.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the fibroblast heatmap report as a string
        
    Example:
        >>> load_fibroblast_heatmap_report("test_patient")
        "Fibroblast distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Fibroblast")


@tool
def load_granulocyte_heatmap_report(patient_id: str) -> str:
    """
    Load granulocyte heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of granulocytes in the tissue sample.
    Granulocytes (neutrophils, eosinophils, basophils) are white blood cells involved 
    in innate immunity and inflammatory responses. Their distribution can indicate 
    areas of inflammation, infection, or immune activation.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the granulocyte heatmap report as a string
        
    Example:
        >>> load_granulocyte_heatmap_report("test_patient")
        "Granulocyte distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Granulocyte")


@tool
def load_il1b_heatmap_report(patient_id: str) -> str:
    """
    Load IL1B gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of IL1B (Interleukin-1 Beta) gene expression 
    levels in the tissue sample. IL1B is a pro-inflammatory cytokine involved in immune 
    responses, inflammation, and tissue damage. High expression can indicate active 
    inflammatory processes or immune activation.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the IL1B heatmap report as a string
        
    Example:
        >>> load_il1b_heatmap_report("test_patient")
        "IL1B expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "IL1B")


@tool
def load_krt7_heatmap_report(patient_id: str) -> str:
    """
    Load KRT7 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of KRT7 (Keratin 7) gene expression levels 
    in the tissue sample. KRT7 is a type II keratin expressed in simple epithelia and 
    some glandular tissues. It's used as a marker for epithelial differentiation and 
    can help identify epithelial cell types and their distribution.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the KRT7 heatmap report as a string
        
    Example:
        >>> load_krt7_heatmap_report("test_patient")
        "KRT7 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "KRT7")


@tool
def load_malignant_bladder_heatmap_report(patient_id: str) -> str:
    """
    Load malignant bladder cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of malignant bladder cells 
    in the tissue sample. These cells represent the cancerous component of bladder tissue 
    and their distribution patterns are crucial for understanding tumor architecture, 
    invasion patterns, and potential areas of aggressive growth.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the malignant bladder cell heatmap report as a string
        
    Example:
        >>> load_malignant_bladder_heatmap_report("test_patient")
        "Malignant bladder cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Malignant_bladder")


@tool
def load_mast_heatmap_report(patient_id: str) -> str:
    """
    Load mast cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of mast cells in the tissue sample.
    Mast cells are immune cells involved in allergic responses, inflammation, and 
    tissue repair. They release histamine and other mediators that can influence 
    local immune responses and tissue remodeling.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the mast cell heatmap report as a string
        
    Example:
        >>> load_mast_heatmap_report("test_patient")
        "Mast cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Mast")


@tool
def load_momac_heatmap_report(patient_id: str) -> str:
    """
    Load monocyte/macrophage heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of monocytes and macrophages 
    in the tissue sample. These cells are key components of the innate immune system 
    involved in phagocytosis, antigen presentation, and tissue homeostasis. Their 
    distribution can indicate areas of immune surveillance and tissue remodeling.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the monocyte/macrophage heatmap report as a string
        
    Example:
        >>> load_momac_heatmap_report("test_patient")
        "Monocyte/macrophage distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "MoMac")


@tool
def load_muscle_heatmap_report(patient_id: str) -> str:
    """
    Load muscle cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of muscle cells in the tissue sample.
    Muscle cells in bladder tissue are primarily smooth muscle cells that control 
    bladder contraction and relaxation. Their distribution patterns can indicate 
    tissue architecture and potential areas of muscle layer involvement in disease.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the muscle cell heatmap report as a string
        
    Example:
        >>> load_muscle_heatmap_report("test_patient")
        "Muscle cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Muscle")


@tool
def load_other_heatmap_report(patient_id: str) -> str:
    """
    Load other cell types heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of other cell types 
    not specifically categorized in the tissue sample. This category may include 
    various stromal cells, immune cells, or other cell populations that don't 
    fit into the main classification categories.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the other cell types heatmap report as a string
        
    Example:
        >>> load_other_heatmap_report("test_patient")
        "Other cell types distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Other")


@tool
def load_pik3ca_heatmap_report(patient_id: str) -> str:
    """
    Load PIK3CA gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of PIK3CA gene expression levels 
    in the tissue sample. PIK3CA encodes the catalytic subunit of PI3K, a key 
    enzyme in the PI3K/AKT/mTOR signaling pathway. Mutations and overexpression 
    are common in various cancers and can indicate activation of survival and 
    proliferation pathways.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the PIK3CA heatmap report as a string
        
    Example:
        >>> load_pik3ca_heatmap_report("test_patient")
        "PIK3CA expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "PIK3CA")


@tool
def load_plasma_heatmap_report(patient_id: str) -> str:
    """
    Load plasma cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of plasma cells in the tissue sample.
    Plasma cells are terminally differentiated B cells that produce antibodies. 
    Their distribution can indicate areas of active humoral immune responses and 
    antibody production, which may be important for understanding local immune 
    responses to disease.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the plasma cell heatmap report as a string
        
    Example:
        >>> load_plasma_heatmap_report("test_patient")
        "Plasma cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "Plasma")


@tool
def load_rb1_heatmap_report(patient_id: str) -> str:
    """
    Load RB1 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of RB1 gene expression levels 
    in the tissue sample. RB1 is a tumor suppressor gene that regulates cell 
    cycle progression. Loss of function or reduced expression can lead to 
    uncontrolled cell proliferation and is associated with various cancers.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the RB1 heatmap report as a string
        
    Example:
        >>> load_rb1_heatmap_report("test_patient")
        "RB1 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "RB1")


@tool
def load_s100a8_heatmap_report(patient_id: str) -> str:
    """
    Load S100A8 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of S100A8 gene expression levels 
    in the tissue sample. S100A8 is a calcium-binding protein involved in 
    inflammation and immune responses. High expression can indicate active 
    inflammatory processes, neutrophil activation, or tissue damage responses.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the S100A8 heatmap report as a string
        
    Example:
        >>> load_s100a8_heatmap_report("test_patient")
        "S100A8 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "S100A8")


@tool
def load_tp53_heatmap_report(patient_id: str) -> str:
    """
    Load TP53 gene expression heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution of TP53 gene expression levels 
    in the tissue sample. TP53 is a critical tumor suppressor gene that regulates 
    cell cycle, apoptosis, and DNA repair. Mutations or altered expression patterns 
    are common in cancer and can indicate genomic instability or loss of tumor 
    suppression mechanisms.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the TP53 heatmap report as a string
        
    Example:
        >>> load_tp53_heatmap_report("test_patient")
        "TP53 expression analysis shows..."
    """
    return _load_heatmap_description(patient_id, "TP53")


@tool
def load_t_nk_heatmap_report(patient_id: str) -> str:
    """
    Load T cell and Natural Killer cell heatmap description from Google Storage bucket for a specific patient.
    
    This report describes the spatial distribution and density of T cells and Natural 
    Killer (NK) cells in the tissue sample. These cells are key components of 
    the adaptive and innate immune systems respectively. T cells mediate cellular 
    immunity while NK cells provide rapid responses to infected or transformed cells.
    
    Args:
        patient_id: The unique identifier for the patient (e.g., 'test_patient')
        
    Returns:
        The content of the T cell and NK cell heatmap report as a string
        
    Example:
        >>> load_t_nk_heatmap_report("test_patient")
        "T cell and NK cell distribution analysis shows..."
    """
    return _load_heatmap_description(patient_id, "T_NK")


def _load_heatmap_description(patient_id: str, feature: str) -> str:
    """
    Helper function to load heatmap report from Google Storage bucket.
    
    Args:
        patient_id: The unique identifier for the patient
        feature: The feature name
        
    Returns:
        The content of the heatmap report as a string
    """
    if patient_id == "test_patient":
        patient_id = "CH_B_030"
    else:
        print(f"Converting patient ID {patient_id} to CH ID")
        patient_id = convert_to_ch_id(patient_id)
    
    try:
        # Initialize GCS filesystem
        fs = gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
        bucket_name = "gdm-hackathon"
        
        # Construct the path to the heatmap description
        description_path = f"{bucket_name}/data/heatmaps/descriptions/{patient_id}_{feature}_description.json"
        
        # Check if the description exists
        if not fs.exists(description_path):
            return f"Error: Heatmap description not found for patient {patient_id} and feature {feature}. Path: {description_path}"
        
        # Read the heatmap description content
        with fs.open(description_path, 'r') as f:
            data = json.load(f)
            
        # Extract the description from the JSON data
        description = data.get("description", "No description found in the file")
        
        return f"Heatmap Description for {patient_id} - {feature}:\n\n{description}"
        
    except Exception as e:
        return f"Error loading heatmap description for patient {patient_id} and feature {feature}: {str(e)}"


# %%
if __name__ == "__main__":
    # Test one of the tools
    print(load_tp53_heatmap_report("test_patient"))

# %%
