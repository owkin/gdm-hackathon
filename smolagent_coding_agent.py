# %%
from smolagents import CodeAgent, FinalAnswerTool
from gdm_hackathon.poc.report_functions import get_clinical_report, get_hipe_report, get_spt_report

from gdm_hackathon.poc.evaluation_tool import evaluate_report_relevance_in_zero_shot
import google.auth
import google.auth.transport.requests
from smolagents import OpenAIServerModel
final_answer_tool = FinalAnswerTool()

PROJECT_ID = "gemma-hcls25par-703"
LOCATION = "europe-west4"
ENDPOINT_ID = "5382630586475085824" # The numeric ID of the endpoint
MODEL_ID_FOR_AGENT = "google/gemma-3-27b-it-mg-one-click-deploy" # The model we deployed

ENDPOINT_URL = (
    f"https://5382630586475085824.europe-west4-797788125421.prediction.vertexai.goog/v1/projects/"
    f"{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
)

# 1. Get the default credentials from your environment
creds, project = google.auth.default()

# 2. Refresh the credentials to get a valid access token
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)
access_token = creds.token


model = OpenAIServerModel(
    model_id=MODEL_ID_FOR_AGENT,
    api_base=ENDPOINT_URL, # Leave this blank to query OpenAI servers.
    api_key=access_token, # Switch to the API key for the server you're targeting.
)

# %%
# Define the coding agent
coding_agent = CodeAgent(
    model=model,
    name="coding_agent",
    description="A coding agent that selects the best 2 tools out of 3 available tools.",
    tools=[get_clinical_report, get_hipe_report, get_spt_report, evaluate_report_relevance_in_zero_shot, final_answer_tool],
    max_steps=6,
)
# %%
# Function to run the coding agent
def run_coding_agent():
    """Run the smolagent coding agent to find the best report combination for survival prediction."""
    response = coding_agent.run(
        r"""
    You are a medical AI coding agent tasked with finding the optimal combination of medical reports for predicting patient survival/treatment response.

    ## Available Tools:
    You have access to 3 different medical report tools, each providing different types of patient information:
    1. **get_clinical_report**: Provides clinical information including patient demographics, cancer diagnosis with TNM staging, ECOG performance status, comorbidities, and treatment plans.
    2. **get_hipe_report**: Provides histology biomarker data with comprehensive immune infiltration analysis, including immune cell composition, spatial distribution, tumor-immune interactions, and microenvironment characteristics.
    3. **get_spt_report**: Provides spatial transcriptomics data with information about the most expressed genes in tumor regions and surrounding tissue, including transcript counts and biological interpretations.

    ## Your Mission:
    Your goal is to determine which combination of 2 reports provides the best information for predicting whether a patient will respond to treatment (survival prediction).

    ## Evaluation Process:
    To evaluate the quality of different report combinations, you have access to the **evaluate_report_relevance_in_zero_shot** tool. This tool:
    - Takes 2 tool names as input, which are the function names of the tools you have access to.
        Usage example: evaluate_report_relevance_in_zero_shot(tool1_name="get_clinical_report", tool2_name="get_hipe_report")
    - Generates combined reports for all patients using those 2 tools
    - Uses MedGemma (a medical AI model) to predict treatment response for each patient
    - Compares predictions against ground truth data
    - Returns an accuracy score showing how well the combined reports predict treatment response

    ## Your Task:
    1. **Investigate each tool**: First, examine what each tool returns by testing them on a test patient, name="patient1" to understand the type and quality of information provided.
    2. **Select the most promising combination**: Select the most promising combination of 2 tools for survival prediction.
    3. **Evaluate the resulting accuracy**: Evaluate the resulting accuracy of the selected combination of 2 tools for survival prediction.
    4. **Iterate at most 3 times step 2 and 3**: Iterate at most 3 times step 2 and 3.
    5. **Provide recommendation**: Based on your analysis, recommend the best combination of 2 tools for survival prediction and explain your reasoning.

    ## Expected Output:
    Your response should include:1"
    - Accuracy scores from evaluating all 3 combinations using evaluate_report_relevance_in_zero_shot
    - Clear recommendation of the best combination
    - Detailed explanation of why this combination is optimal for survival prediction

    ## Important Notes:
    - A "full report" consists of exactly 2 sub-reports combined
    - The goal is to maximize the accuracy of treatment response prediction
    - Consider both the clinical relevance and the complementary nature of the information
    - The evaluation tool uses real patient data and MedGemma predictions, so the results are meaningful

    Start by investigating each tool, then systematically evaluate all combinations to find the optimal pair for survival prediction.
    """

    )
    return response

if __name__ == "__main__":
    result = run_coding_agent()
    print(result) 
# %%
