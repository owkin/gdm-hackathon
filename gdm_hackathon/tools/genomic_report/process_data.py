# %%

from engine_features.patient.loading.mosaic.wes import load_wes
import json
import requests
from datetime import datetime
import gcsfs
from gdm_hackathon.config import GCP_PROJECT_ID

patient_ids = ['CH_B_030a', 'CH_B_033a', 'CH_B_037a', 'CH_B_041a', 'CH_B_046a', 'CH_B_059a', 'CH_B_062a', 'CH_B_064a', 'CH_B_068a', 'CH_B_069a', 'CH_B_073a', 'CH_B_074a', 'CH_B_075a', 'CH_B_079a', 'CH_B_087a']

def save_mutated_genes(patient_id: str, mutated_genes: list, data_type: str, output_dir: str = "mutated_genes"):
    """
    Save the mutated genes list to a JSON file locally.
    
    Args:
        patient_id: The unique identifier for the patient
        mutated_genes: List of mutated gene names
        data_type: Type of genomic data (snv_indel, cnv, cna, etc.)
        output_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the data structure
    genes_data = {
        "patient_id": patient_id,
        "data_type": data_type,
        "mutated_genes": mutated_genes,
        "generated_at": datetime.now().isoformat(),
        "total_mutations": len(mutated_genes)
    }
    
    # Save the data to a JSON file
    output_path = f"{output_dir}/{patient_id}_{data_type}_genes.json"
    
    with open(output_path, 'w') as f:
        json.dump(genes_data, f, indent=2)
    
    return output_path

def process_data_type(data_type: str):
    """
    Process a specific data type for all patients.
    
    Args:
        data_type: Type of genomic data to process (snv_indel, cnv, cna, gii, tmb)
    """
    print(f"\nProcessing {data_type.upper()} data for all patients...")
    print("=" * 60)
    
    # Load data for the specific type
    df = load_wes("Bladder", "CHUV", gene_nomenclature="gene_name", data_type=data_type)
    if data_type in ['gii', 'tmb']:
        df = df.set_index("sample_id")
    df = df.loc[patient_ids]
    
    for patient in df.index:
        print(f"\nProcessing patient: {patient}")
        
        # For different data types, we need different logic to extract relevant genes
        if data_type in ["snv_indel", "cnv"]:
            # Binary matrix - filter columns where value is not 0
            mutated_genes = df.loc[patient].index[df.loc[patient] != 0].tolist()
        elif data_type == "cna":
            # CNA has values -1 (deletion), 1 (amplification), 0 (no alteration)
            # Get genes with any alteration (non-zero values)
            mutated_genes = df.loc[patient].index[df.loc[patient] != 0].tolist()
        elif data_type in ["gii", "tmb"]:
            # These are scores, not gene lists, so we'll create a sentence with the score
            score_value = df.loc[patient].iloc[0] if len(df.loc[patient]) == 1 else df.loc[patient]
            score_sentence = f"The {data_type.upper()} value for patient {patient} is {score_value}"
            mutated_genes = [score_sentence]  # Store as a single-item list for consistency
        else:
            print(f"Unknown data type: {data_type}")
            continue
        
        print(f"Found {len(mutated_genes)} affected genes: {', '.join(mutated_genes[:10])}{'...' if len(mutated_genes) > 10 else ''}")
        
        # Save the mutated genes locally
        local_path = save_mutated_genes(patient, mutated_genes, data_type)
        print(f"{data_type.upper()} genes saved locally to: {local_path}")
        
        print("-" * 60)

# %%

# Process different data types
data_types = ["snv_indel", "cnv", "cna", "gii", "tmb"]

for data_type in data_types:
    process_data_type(data_type)

print("\nAll genomic data has been processed, saved locally, and uploaded to the bucket!")

# %%
