"""Utility functions for the project."""

def convert_to_mw_id(patient_id: str) -> str:
    """Convert the patient ID to the MW ID format."""
    mapping = {
        "CH_B_030a": "MW_B_001a",
        "CH_B_033a": "MW_B_002a",
        "CH_B_037a": "MW_B_003a",
        "CH_B_041a": "MW_B_014a",
        "CH_B_046a": "MW_B_004a",
        "CH_B_059a": "MW_B_005a",
        "CH_B_062a": "MW_B_006a",
        "CH_B_064a": "MW_B_007a",
        "CH_B_068a": "MW_B_008a",
        "CH_B_069a": "MW_B_009a",
        "CH_B_073a": "MW_B_015a",
        "CH_B_074a": "MW_B_010a",
        "CH_B_075a": "MW_B_011a",
        "CH_B_079a": "MW_B_012a",
        "CH_B_087a": "MW_B_013a",
    }
    return mapping[patient_id]