# gdm-hackathon


## Biomarker discovery

Extract interpertable and predictive signal from multi-modal data.



# Set up

- Download the gcloud cli https://cloud.google.com/sdk/docs/install-sdk
- Set the project and authenticate (with your hackathon account)
```bash
gcloud config set project gemma-hcls25par-703
gcloud auth login
```

- Install the dependencies
```bash
uv venv --python 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Hackathon To-Do List

### 1. Environment & Setup (`uv`, GCP)

-   **[✅] Init Project:** Clone the repo. Everyone gets access to the GCP project.
-   **[ ] Install Deps:** We're using `uv`. Create a `pyproject.toml` or `requirements.txt` and install dependencies.
    ```bash
    # Install uv first if you haven't
    pip install uv
    
    # Create a virtual environment and install deps
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt # (e.g., google-cloud-aiplatform, pandas, tqdm)
    ```
-   **[ ] Deploy/Access Models:** The models are foundation endpoints on Vertex AI / Gemini.

### 2. Data Wrangling

-   **[ ] Create Data Manifest?:** Yaml file with all data files for each patient. Multiple modalities per patient.
-   **[ ] Build Data Loader:** Write a Python function `get_patient_data(patient_id)` that reads the manifest and loads all data for one patient into a structured object or dictionary.

### 3. The Core Engine

![image](workflow.png)

-   **[ ] Each branch on the left is an agent from data loading to text description:** If the data is computed separately, the agent is a simple loading function. Each agent may call python functions or API endpoints. All agents should cache the results.
    -   **[ ] HIPE reports:** Either load the report, or call the text description model from the aggregated results csv.
    -   **[ ] Mpp4 Image description:** Cut the image, set the correct resolution, call multimodal model.
    -   **[ ] Spt RNA-seq:** Load the spatial rna-seq, aggregate to patient-level, call text description model.
    -   **[ ] Spatialized exression data:** Load the spatial rnas-seq, plot the gene expression heatmap, call multimodal model.
    -   **[ ] Clinical notes:** Load the clinical data, call text description model.
-   **[ ] Genetic algorithm loop:** Call the agents, aggregate the results, call the fitness model.
    -   **[ ] Orchestrator description model:** Merge the text descriptions into a single text prompt.
    -   **[ ] Predictor model:** Call the predictor model with the prompt and the orchestrator description.
    -   **[ ] Fitness model:** Compute c-index / accuracy of the predictor model.


We may optimize on the tool call of the orchestrator model.

### 4. 

-   **[ ] Frontend?** Build a simple frontend to visualize the result from multimodal data to clinical endpoint prediction
-   **[ ] Target discovery?** Use TxGemma to discover targets from the description.