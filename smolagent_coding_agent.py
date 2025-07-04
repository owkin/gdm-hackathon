# %%
from smolagents import CodeAgent, FinalAnswerTool
from gdm_hackathon.models.vertex_models import get_model

from gdm_hackathon.tools.evaluation_tool import evaluate_report_relevance_in_zero_shot

from gdm_hackathon.tools import (
load_histopathological_immune_infiltration_report,
load_histopathological_tumor_stroma_compartments_report,
load_histopathological_tumor_nuclear_morphometry_report,
)

from gdm_hackathon.tools import (
load_clinical_report,
)

from gdm_hackathon.tools import (
load_cdk12_heatmap_report, 
load_dc_heatmap_report,
load_b_cell_heatmap_report,
load_egfr_heatmap_report,
load_erbb2_heatmap_report,
load_endothelial_heatmap_report,
load_epithelial_heatmap_report,
load_fgfr3_heatmap_report,
load_fibroblast_heatmap_report,
load_granulocyte_heatmap_report,
load_il1b_heatmap_report,
load_krt7_heatmap_report,
load_malignant_bladder_heatmap_report,
load_mast_heatmap_report,
load_momac_heatmap_report,
load_muscle_heatmap_report,
load_other_heatmap_report,
load_pik3ca_heatmap_report,
load_plasma_heatmap_report,
load_rb1_heatmap_report,
load_s100a8_heatmap_report,
load_tp53_heatmap_report,
load_t_nk_heatmap_report,
load_snv_indel_genomic_report,
load_cnv_genomic_report,
load_cna_genomic_report,
load_gii_genomic_report,
load_tmb_genomic_report,
load_fgfr3_pathway_report,
load_egfr_pathway_report,
load_pi3k_pathway_report,
load_anti_pd1_pathway_report,
load_tgf_beta_pathway_report,
load_hypoxia_pathway_report,
load_emt_pathway_report,
load_cell_cycle_pathway_report,
load_ddr_deficiency_pathway_report,
load_p53_pathway_report,
)

final_answer_tool = FinalAnswerTool()

# %%

model = get_model("gemma-3-27b")

# %%
# Define the coding agent
coding_agent = CodeAgent(
    model=model,
    name="coding_agent",
    description="A coding agent that selects the best 2 tools out of 3 available tools.",
    tools=[
        evaluate_report_relevance_in_zero_shot, # evaluation tool
        # # spatial transcriptomics heatmap tools (cell type  / gene expression specific)
        load_cdk12_heatmap_report, 
        load_dc_heatmap_report,
        load_b_cell_heatmap_report,
        load_egfr_heatmap_report,
        load_erbb2_heatmap_report,
        load_endothelial_heatmap_report,
        load_epithelial_heatmap_report,
        load_fgfr3_heatmap_report,
        load_fibroblast_heatmap_report,
        load_granulocyte_heatmap_report,
        load_il1b_heatmap_report,
        load_krt7_heatmap_report,
        load_malignant_bladder_heatmap_report,
        load_mast_heatmap_report,
        load_momac_heatmap_report,
        load_muscle_heatmap_report,
        load_other_heatmap_report,
        load_pik3ca_heatmap_report,
        load_plasma_heatmap_report,
        load_rb1_heatmap_report,
        load_s100a8_heatmap_report,
        load_tp53_heatmap_report,
        load_t_nk_heatmap_report,
        # histopathological report family
        load_histopathological_immune_infiltration_report,
        load_histopathological_tumor_stroma_compartments_report,
        load_histopathological_tumor_nuclear_morphometry_report,
        # genomic report family
        load_snv_indel_genomic_report,
        load_cnv_genomic_report,
        load_cna_genomic_report,
        load_gii_genomic_report,
        load_tmb_genomic_report,
        # bulk RNAseq report family
        load_fgfr3_pathway_report,
        load_egfr_pathway_report,
        load_pi3k_pathway_report,
        load_anti_pd1_pathway_report,
        load_tgf_beta_pathway_report,
        load_hypoxia_pathway_report,
        load_emt_pathway_report,
        load_cell_cycle_pathway_report,
        load_ddr_deficiency_pathway_report,
        load_p53_pathway_report,
        final_answer_tool,
        # clinical report
        load_clinical_report
        ],
    max_steps=50,  # Increased from 20 to 50
)
# %%
# Function to run the coding agent
def run_coding_agent():
    """Run the smolagent coding agent to find the best report combination for survival prediction."""
    response = coding_agent.run(
        r"""
    You are a biomedical AI coding agent tasked with finding the optimal combination of medical reports for predicting patient survival response.

    ## Available Tools:
    You have access to several medical report tools, which can be classified into different families:
    1. **Spatial transcriptomics heatmaps** (load_{celltype}_heatmap_report): Cell type distribution in tissue
    2. **Histopathological reports** (load_histopathological_{type}_report): Tissue analysis
    3. **Clinical reports** (load_clinical_report): Patient clinical data
    4. **Pathway reports** (load_{pathway}_pathway_report): RNA-seq pathway analysis
    5. **Genomic reports** (load_{type}_genomic_report): Genomic analysis

    ## Your Mission:
    Find the best combination of 2 reports for predicting patient treatment response (survival prediction).

    ## Evaluation Process:
    Use **evaluate_report_relevance_in_zero_shot** to test combinations:
    - Takes 2 tool names as input
    - Example: evaluate_report_relevance_in_zero_shot(tool1_name="load_cdk12_heatmap_report", tool2_name="load_dc_heatmap_report")
    - Returns accuracy score for treatment response prediction

    ## Efficient Strategy (IMPORTANT):
    You have 50 steps maximum. Be strategic:
    1. **Quick exploration** (5-10 steps): Test 2-3 diverse combinations from different families
    2. **Focus on promising families** (20-30 steps): Based on initial results, focus on the most promising report families
    3. **Optimize within families** (10-15 steps): Test variations within the best-performing families
    4. **Final evaluation** (5 steps): Confirm the best combination and provide final answer

    ## Task Breakdown:
    1. **Start with diverse combinations**: Test one combination from each major family (spatial, histopathological, clinical, pathway, genomic)
    2. **Identify best families**: Focus on families that show higher accuracy
    3. **Systematic testing**: Test combinations within the best families
    4. **Final recommendation**: Use final_answer_tool with your best combination

    ## Expected Output:
    - Best accuracy score found
    - Clear recommendation of the optimal 2-tool combination
    - Brief explanation of why this combination works best

    ## Important Notes:
    - Each evaluation uses real patient data and MedGemma predictions
    - Focus on accuracy scores - higher is better
    - Don't waste steps on obvious poor combinations
    - Use final_answer_tool when you have a clear winner

    Start with a quick test of diverse combinations to understand the landscape, then focus your efforts strategically.

    Your first output should be a test:

    Thought: I will proceed step by step and test the tool load_cdk12_heatmap_report on test_patient. 
    <code>
    print(load_cdk12_heatmap_report("test_patient"))
    print(load_histopathological_immune_infiltration_report("test_patient"))
    print(load_clinical_report("test_patient"))
    </code>

    Let begin ! 
    """

    )
    return response

if __name__ == "__main__":
    result = run_coding_agent()
    print(result) 
# %%
