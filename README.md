# gdm-hackathon
=======

# Project: Evolving Insight
### A Multi-Modal Prompt Discovery System for Clinical Predictions

Our goal is to use a genetic algorithm to discover the optimal text prompt that guides a frozen LLM to make accurate clinical predictions from multi-modal patient data. We do not train any models; we "train" the prompt.

---

## Hackathon To-Do List

### 1. Environment & Setup (`uv`, GCP)

-   **[ ] Init Project:** Clone the repo. Everyone gets access to the GCP project.
-   **[ ] Install Deps:** We're using `uv`. Create a `pyproject.toml` or `requirements.txt` and install dependencies.
    ```bash
    # Install uv first if you haven't
    pip install uv
    
    # Create a virtual environment and install deps
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt # (e.g., google-cloud-aiplatform, pandas, tqdm)
    ```
-   **[ ] GCP Authentication:** Authenticate your local environment to access Google Cloud APIs.
    ```bash
    gcloud auth application-default login
    gcloud config set project [your-gcp-project-id]
    ```
-   **[ ] Deploy/Access Models:** We don't deploy, we *access*. The models are foundation endpoints on Vertex AI.
    -   Enable the "Vertex AI API" in the GCP console.

### 2. Data Wrangling (The Multi-Modal Challenge)

-   **[ ] Acknowledge Complexity:** This will take time. The goal is a unified data interface.
-   **[ ] Create Data Manifest:** Create a central `data/manifest.csv`. This is our source of truth. It links all data modalities for a given patient.
    -   **Columns:** `patient_id`, `wsi_image_path`, `genomic_data_path`, `clinical_notes_path`, `ground_truth_response`
-   **[ ] Build Data Loader:** Write a Python function `get_patient_data(patient_id)` that reads the manifest and loads all data for one patient into a structured object or dictionary.

### 3. The Core Engine (The "Fitness Function")

-   **[ ] Design the Prompt Structure:** The GA will evolve a prompt. Let's make it structured (e.g., a JSON object or a formatted string) so it can reference different data types.
    -   *Example Evolved Prompt:* `"Analyze the following patient. Focus on the spatial arrangement of lymphocytes in the WSI. Correlate this with the provided genomic data to predict immunotherapy response."*
-   **[ ] Build the Pipeline Function:** Create the function `calculate_fitness(prompt)` which performs the *entire* evaluation.
    1.  It takes one candidate prompt as input.
    2.  It loops through a validation set of `patient_id`s from our manifest.
    3.  **For each patient:**
        -   It calls our `get_patient_data()` function.
        -   It dynamically constructs a "mega-prompt" for Gemini, combining the candidate prompt, the patient's clinical notes, genomic data (as text), and the histopathology image.
        -   It calls the Vertex AI Gemini 1.5 Pro endpoint with this multi-modal input.
        -   It parses the model's prediction ("Responds" / "Does not Respond").
    4.  It calculates the overall accuracy against the ground truth labels. This accuracy score *is* the fitness of the prompt.

### 4. Evolve & Discover

-   **[ ] Implement the Genetic Algorithm:**
    -   **Population:** Generate an initial population of 50-100 hand-written and randomly generated prompts.
    -   **Selection/Crossover/Mutation:** Implement the logic to create new generations of prompts by combining the best-performing ones and adding random variations.
-   **[ ] Launch the Run:** Execute the main script (`python evolve.py`) to start the evolutionary process. Log the best prompt and its fitness score from each generation.
-   **[ ] Analyze the Winner:** Once the run completes, examine the final, highest-scoring prompt. This is our "discovered" biomarker/feature set.

### 5. ????

-   **[ ] Build the Presentation Deck:** Create the slides telling our story.
    -   **Key Slides:** System Architecture, The "Evolution" Graph (fitness over generations), and the side-by-side "Hero" example showing a bad prompt vs. our evolved prompt on the same patient data.
-   **[ ] Rehearse the Pitch:** Nail the narrative. We didn
