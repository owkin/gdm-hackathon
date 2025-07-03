# HIPE Report Tool

A simple smolagent tool that loads HIPE report data from Google Cloud Storage bucket.

## Features

- Uses the `@tool` decorator from smolagents
- Takes only a patient ID as input
- Automatically constructs the path to the report in the GCP bucket
- Handles multiple possible file paths for flexibility
- Provides clear error messages if files are not found
- Works with Vertex AI models via custom VertexAIServerModel

## Usage

### Basic Usage

```python
from gdm_hackathon.tools.hipe_report.hipe_tool import load_hipe_report

# Load a HIPE report for a specific patient
result = load_hipe_report("TCGA-2F-A9KO-01Z-00-DX1")
print(result)
```

### With smolagents CodeAgent and Vertex AI

```python
from smolagents import CodeAgent
from gdm_hackathon.tools.hipe_report.hipe_tool import load_hipe_report
from gdm_hackathon.models.vertex_ai_model import VertexAIServerModel

# Create a Vertex AI model
model = VertexAIServerModel(
    model_id="medgemma",
    project_id="gemma-hcls25par-703",
    location="europe-west4",
    endpoint_id="4761133837897957376",
)

# Create an agent with the HIPE report tool
agent = CodeAgent(
    tools=[load_hipe_report],
    model=model,
    name="hipe_report_agent"
)

# Use the agent to load a report
result = agent.run("Load the HIPE report for TCGA-2F-A9KO-01Z-00-DX1")
print(result)
```

### With default InferenceClientModel

```python
from smolagents import CodeAgent, InferenceClientModel
from gdm_hackathon.tools.hipe_report.hipe_tool import load_hipe_report

# Create an agent with the HIPE report tool
model = InferenceClientModel()
agent = CodeAgent(
    tools=[load_hipe_report],
    model=model,
    name="hipe_report_agent"
)

# Use the agent to load a report
result = agent.run("Load the HIPE report for TCGA-2F-A9KO-01Z-00-DX1")
print(result)
```

## File Path Structure

The tool searches for files that start with the patient ID in the following directories (in order of preference):

1. `gdm-hackathon/hipe_reports/TCGA_BLCA/` - looks for files starting with `{patient_id}`
2. `gdm-hackathon/hipe_reports/` - looks for files starting with `{patient_id}`

For example, if patient_id is `TCGA-2F-A9KO-01Z-00-DX1`, it will find files like:
- `TCGA-2F-A9KO-01Z-00-DX1.195576CF-B739-4BD9-B15B-4A70AE287D3E.txt`

## Configuration

The tool uses the `GCP_PROJECT_ID` from `gdm_hackathon.config`. Make sure this is set to your GCP project ID.

## Testing

Run the test script to verify the tool works:

```bash
python gdm_hackathon/tools/hipe_report/test_tool.py
```

The test script will:
1. Test the tool directly
2. Create an agent with the Vertex AI model
3. Test the agent with a sample patient ID

## Example

```python
# Input
patient_id = "TCGA-2F-A9KO-01Z-00-DX1"

# Output
"HIPE Report for TCGA-2F-A9KO-01Z-00-DX1:

[Report content here...]"
```
