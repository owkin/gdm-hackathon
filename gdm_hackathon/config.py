# config.py

# --- GCP & Vertex AI Configuration ---
GCP_PROJECT_ID = "gemma-hcls25par-703"
GCP_LOCATION = "europe-west4"
VERTEX_MODEL_NAME = "gemini-1.5-pro-001"

# --- Data Configuration ---
DATA_MANIFEST_PATH = "data/manifest.yaml"

# --- Genetic Algorithm Configuration ---
POPULATION_SIZE = 50
NUM_GENERATIONS = 20
FITNESS_VALIDATION_SUBSET_SIZE = 10 
NUM_ELITES = 5 