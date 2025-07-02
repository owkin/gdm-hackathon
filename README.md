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

This way you should be able to push data to our bucket:
```bash
gsutil cp test gs://gdm-hackathon/test
```

## Spawn a VM on GCP

Go to Compute Engine: In the GCP Console, navigate to Compute Engine -> VM instances.

Create Instance:
- Name: hackathon-workbench.
- Region: eu-west-4
- Machine configuration -> GPU:
    - Click Add GPU.
    - GPU Type: NVIDIA T4 (g4 series)
    - Number of GPUs: 1
- Boot disk -> Change: This is the most important step.
    - Click Change. A new panel will open.
    - Operating system : Deep Learning on Linux
    - Version : I chose "Deep Learning VM for PyTorch 2.4 with CUDA 12.4 M129" (last one)
    - Increase disk size
- Networking: Check the box for Allow HTTP traffic and Allow HTTPS traffic. This is essential to access the web-based IDE.
- Security -> Service Account: Ensure it is set to Compute Engine default service account and that the Access Scope is Allow full access to all Cloud APIs. This lets the VM easily talk to your storage bucket.

Click Create. It will take a few minutes to provision.

You can then connect to the VM via ssh.

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