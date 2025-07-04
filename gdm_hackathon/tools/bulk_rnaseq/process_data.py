# %%

from engine_features.patient.loading.mosaic.rnaseq import load_rnaseq
from engine_features.scoring.dea.score_gene_set import GeneSetScoring
import json
import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Dict, List, Tuple, Literal, Optional

from gdm_hackathon.utils import convert_to_mw_id

# Patient IDs
patient_ids = ['CH_B_030', 'CH_B_033', 'CH_B_037', 'CH_B_041', 'CH_B_046', 'CH_B_059', 'CH_B_062', 'CH_B_064', 'CH_B_068', 'CH_B_069', 'CH_B_073', 'CH_B_074', 'CH_B_075', 'CH_B_079', 'CH_B_087']

# Define gene signatures
SIGNATURES = {
    "fgfr3": ["FGFR3", "FGF1", "FGF2", "FRS2", "GRB2", "SOS1", "HRAS", "KRAS", "BRAF", "MAP2K1", "MAPK1", "PIK3CA", "PIK3R1", "AKT1", "PLCG1", "STAT3", "PTPN11"],
    "egfr": ["EGFR", "EGF", "TGFA", "AREG", "EREG", "HBEGF", "BTC", "ERBB2", "ERBB3", "GRB2", "SOS1", "SHC1", "CBL", "GAB1", "STAT3", "STAT5A", "PIK3CA", "AKT1", "MAPK1", "MAPK3"],
    "pi3k": ["PIK3CA", "PIK3CB", "PIK3R1", "PIK3R2", "PTEN", "AKT1", "AKT2", "AKT3", "MTOR", "RPS6KB1", "EIF4EBP1", "GSK3B", "FOXO1", "FOXO3", "CDKN1B"],
    "anti_pd1": ["CCL5", "CD27", "CD274", "CD276", "CD8A", "CMKLR1", "CXCL9", "CXCR6", "HLA-DQA1", "HLA-DRB1", "HLA-E", "IDO1", "LAG3", "NKG7", "PDCD1LG2", "PSMB10", "STAT1", "TIGIT"],
    "tgf_beta": ["TGFB1", "TGFB2", "TGFB3", "TGFBR1", "TGFBR2", "SMAD2", "SMAD3", "SMAD4", "SMAD7", "SKI", "SKIL", "ID1", "SERPINE1", "COL1A1", "THBS1"],
    "hypoxia": ["HIF1A", "EPAS1", "ARNT", "VEGFA", "ADM", "ALDOA", "BNIP3", "CA9", "ENO1", "EGLN1", "HK2", "LDHA", "NDRG1", "P4HA1", "PDK1", "PGK1", "SLC2A1"],
    "emt": ["FN1", "VIM", "CDH2", "SNAI1", "SNAI2", "TWIST1", "ZEB1", "ZEB2", "MMP2", "MMP9", "COL1A1", "COL5A2", "ITGAV", "ITGB6", "SERPINE1", "TGFB1", "WNT5A", "ACTA2", "TAGLN", "SPARC"],
    "cell_cycle": ["CDC20", "CDK1", "CCNA2", "CCNB1", "CCNB2", "PLK1", "BUB1", "BUB1B", "PTTG1", "AURKA", "AURKB", "CENPA", "CENPE", "CENPF", "KIF2C", "TOP2A", "NUSAP1", "CDKN3", "CDC25C", "ESPL1"],
    "ddr_deficiency": ["ATM", "ATR", "BRCA1", "BRCA2", "PALB2", "FANCA", "FANCC", "ERCC2", "MLH1", "MSH2", "MSH6", "PMS2", "RAD51", "CHEK2"],
    "p53": ["TP53", "MDM2", "CDKN1A", "GADD45A", "BAX", "PMAIP1", "BBC3", "DDB2", "RPS27L", "SESN1", "SESN2", "XPC", "ZMAT3", "POLH"]
}

def save_patient_signature_scores(patient_id: str, signature_scores: Dict[str, float], output_dir: str = "rnaseq_signatures"):
    """
    Save the signature scores for a single patient to a JSON file.
    
    Args:
        patient_id: The unique identifier for the patient
        signature_scores: Dictionary of signature names and their scores
        output_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the data structure
    signature_data = {
        "patient_id": convert_to_mw_id(patient_id),
        "original_patient_id": patient_id,
        "signature_scores": signature_scores,
        "method": "SSGSEA",
        "generated_at": datetime.now().isoformat(),
        "total_signatures": len(signature_scores)
    }
    
    # Save the data to a JSON file
    output_path = f"{output_dir}/{patient_id}_signature_scores.json"
    
    with open(output_path, 'w') as f:
        json.dump(signature_data, f, indent=2)
    
    return output_path

def create_patient_set_from_dataframe(df_rnaseq: pd.DataFrame):
    """
    Create a mock PatientSet object from the RNAseq dataframe.
    This is a simplified version to work with the GeneSetScoring class.
    """
    class MockPatientSet:
        def __init__(self, df):
            self.df = df
            self.features = {"rnaseq": MockFeature(df)}
            
        def get_subgroup_dataframes(self, idx=None, keys=None, apply_transform=True):
            if idx is not None:
                df_subset = self.df.loc[idx]
            else:
                df_subset = self.df
            return {"rnaseq": MockFeature(df_subset)}, None
    
    class MockFeature:
        def __init__(self, df):
            self.data = df
    
    return MockPatientSet(df_rnaseq)

def calculate_signature_score(df_rnaseq: pd.DataFrame, signature_name: str, signature_genes: List[str]) -> Dict[str, float]:
    """
    Calculate SSGSEA signature scores for all patients.
    
    Args:
        df_rnaseq: RNAseq dataframe with patients as rows and genes as columns
        signature_name: Name of the signature
        signature_genes: List of genes in the signature
        
    Returns:
        Dictionary mapping patient IDs to signature scores
    """
    try:
        # Create a mock patient set
        patient_set = create_patient_set_from_dataframe(df_rnaseq)
        
        # Initialize the GeneSetScoring class with SSGSEA method
        scoring = GeneSetScoring(
            gene_set=signature_genes,
            score_format="patient",
            method="SSGSEA",
            gene_set_name=signature_name,
            use_patient_set_transform=False,  # We're working with preprocessed data
            corr_threshold=0.05  # Lower threshold to be more permissive
        )
        
        # Calculate gene set activities
        gene_set_activities = scoring.compute_gene_set_activity(patient_set, idx=None)
        
        if gene_set_activities is None:
            print(f"  Warning: Could not calculate {signature_name} scores - insufficient data")
            return {patient_id: np.nan for patient_id in df_rnaseq.index}
        
        # Convert to dictionary
        scores_dict = gene_set_activities.to_dict()
        return scores_dict
        
    except Exception as e:
        print(f"  Error calculating {signature_name} scores: {e}")
        return {patient_id: np.nan for patient_id in df_rnaseq.index}

def process_all_signatures(df_rnaseq: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Process all signatures using SSGSEA method.
    
    Args:
        df_rnaseq: RNAseq dataframe
        
    Returns:
        Dictionary: {signature_name: {patient_id: score}}
    """
    print(f"\nProcessing signatures using SSGSEA method...")
    print("-" * 50)
    
    all_results = {}
    
    for signature_name, signature_genes in SIGNATURES.items():
        print(f"  Calculating {signature_name} signature...")
        
        # Check how many genes are available
        available_genes = [gene for gene in signature_genes if gene in df_rnaseq.columns]
        missing_genes = [gene for gene in signature_genes if gene not in df_rnaseq.columns]
        
        print(f"    Found {len(available_genes)}/{len(signature_genes)} genes")
        if missing_genes:
            print(f"    Missing: {', '.join(missing_genes[:5])}{'...' if len(missing_genes) > 5 else ''}")
        
        if len(available_genes) < 3:
            print(f"    Skipping {signature_name} - insufficient genes ({len(available_genes)} < 3)")
            all_results[signature_name] = {patient_id: np.nan for patient_id in df_rnaseq.index}
            continue
        
        # Calculate scores
        scores = calculate_signature_score(df_rnaseq, signature_name, available_genes)
        all_results[signature_name] = scores
        
        # Print summary statistics
        valid_scores = [s for s in scores.values() if not np.isnan(s)]
        if valid_scores:
            print(f"    Score range: {np.min(valid_scores):.4f} to {np.max(valid_scores):.4f}")
            print(f"    Mean score: {np.mean(valid_scores):.4f}")
        else:
            print(f"    No valid scores calculated")
    
    return all_results

def save_results_per_patient(all_results: Dict[str, Dict[str, float]], output_dir: str = "rnaseq_signatures"):
    """
    Save results per patient - each patient gets their own file with all signature scores.
    
    Args:
        all_results: Results from process_all_signatures
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all patient IDs
    all_patients = set()
    for signature_scores in all_results.values():
        all_patients.update(signature_scores.keys())
    
    # Create per-patient files
    for patient_id in all_patients:
        patient_signatures = {}
        for signature_name, signature_scores in all_results.items():
            if patient_id in signature_scores:
                patient_signatures[signature_name] = signature_scores[patient_id]
            else:
                patient_signatures[signature_name] = np.nan
        
        # Save individual patient file
        save_patient_signature_scores(patient_id, patient_signatures, output_dir)
    
    # Also save a summary file with all patients
    summary_output_path = f"{output_dir}/all_patients_summary.json"
    
    summary_data = {
        "method": "SSGSEA",
        "all_patients": {patient_id: {sig: all_results[sig].get(patient_id, np.nan) 
                                    for sig in SIGNATURES.keys()} 
                        for patient_id in all_patients},
        "signatures": list(SIGNATURES.keys()),
        "generated_at": datetime.now().isoformat(),
        "total_patients": len(all_patients)
    }
    
    with open(summary_output_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"Saved summary results to: {summary_output_path}")

def main():
    """
    Main function to process RNAseq data and calculate signature scores using SSGSEA.
    """
    print("Loading RNAseq data...")
    print("=" * 60)
    
    # Load RNAseq data
    try:
        df_rnaseq = load_rnaseq(
            indication="Bladder",
            cohorts="CHUV",
            normalization="tpm",
            gene_nomenclature="gene_name",
            reindex_patient_id=True,
        )
        print(f"Loaded RNAseq data with shape: {df_rnaseq.shape}")
        print(f"Available patients: {len(df_rnaseq.index)}")
        
    except Exception as e:
        print(f"Error loading RNAseq data: {e}")
        return
    
    # Filter to our patient list
    available_patients = [pid for pid in patient_ids if pid in df_rnaseq.index]
    missing_patients = [pid for pid in patient_ids if pid not in df_rnaseq.index]
    
    print(f"\nFound {len(available_patients)} patients in RNAseq data")
    if missing_patients:
        print(f"Missing patients: {missing_patients}")
    
    # Filter dataframe to available patients
    df_rnaseq_filtered = df_rnaseq.loc[available_patients]
    print(f"Filtered RNAseq data shape: {df_rnaseq_filtered.shape}")
    
    # Process signatures using SSGSEA method
    all_results = process_all_signatures(df_rnaseq_filtered)
    
    # Save results per patient
    save_results_per_patient(all_results)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Processed {len(available_patients)} patients")
    print(f"Calculated {len(SIGNATURES)} signatures using SSGSEA method")
    
    # Print summary statistics
    print(f"\nSignature Score Summary:")
    print("-" * 40)
    for signature_name in SIGNATURES.keys():
        if signature_name in all_results:
            scores = [s for s in all_results[signature_name].values() if not np.isnan(s)]
            if scores:
                print(f"{signature_name:15}: mean={np.mean(scores):.4f}, std={np.std(scores):.4f}, min={np.min(scores):.4f}, max={np.max(scores):.4f}")
            else:
                print(f"{signature_name:15}: No valid scores")

# %%
if __name__ == "__main__":
    main()

# %% 