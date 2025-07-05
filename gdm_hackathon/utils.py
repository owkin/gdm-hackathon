"""Utility functions for the project."""

from functools import lru_cache
import gcsfs
from gdm_hackathon.config import GCP_PROJECT_ID


def convert_to_ch_id(patient_id: str) -> str:
    """Convert the patient ID to the CH ID format."""
    mapping = {
        "CH_B_030": "MW_B_001",
        "CH_B_033": "MW_B_002",
        "CH_B_037": "MW_B_003",
        "CH_B_041": "MW_B_014",
        "CH_B_046": "MW_B_004",
        "CH_B_059": "MW_B_005",
        "CH_B_062": "MW_B_006",
        "CH_B_064": "MW_B_007",
        "CH_B_068": "MW_B_008",
        "CH_B_069": "MW_B_009",
        "CH_B_073": "MW_B_015",
        "CH_B_074": "MW_B_010",
        "CH_B_075": "MW_B_011",
        "CH_B_079": "MW_B_012",
        "CH_B_087": "MW_B_013",
    }

    reverse_mapping = {v: k for k, v in mapping.items()}
    return reverse_mapping[patient_id]

def convert_to_mw_id(patient_id: str) -> str:
    """Convert the patient ID to the MW ID format."""
    if patient_id.endswith("a"):
        patient_id = patient_id[:-1]

    mapping = {
        "CH_B_030": "MW_B_001",
        "CH_B_033": "MW_B_002",
        "CH_B_037": "MW_B_003",
        "CH_B_041": "MW_B_014",
        "CH_B_046": "MW_B_004",
        "CH_B_059": "MW_B_005",
        "CH_B_062": "MW_B_006",
        "CH_B_064": "MW_B_007",
        "CH_B_068": "MW_B_008",
        "CH_B_069": "MW_B_009",
        "CH_B_073": "MW_B_015",
        "CH_B_074": "MW_B_010",
        "CH_B_075": "MW_B_011",
        "CH_B_079": "MW_B_012",
        "CH_B_087": "MW_B_013",
    }

    return mapping[patient_id]

@lru_cache(maxsize=1)
def get_gcs_fs():
    # Initialize GCS filesystem
    return gcsfs.GCSFileSystem(project=GCP_PROJECT_ID)
