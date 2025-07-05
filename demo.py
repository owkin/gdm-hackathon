# %%
from smolagents import CodeAgent, FinalAnswerTool
from gdm_hackathon.models.vertex_models import get_model

from gdm_hackathon.tools.evaluation_tool import evaluate_report_relevance_in_zero_shot, seed_genetic_algorithm

from gdm_hackathon.tools import (
load_histopathological_immune_infiltration_report,
load_histopathological_tumor_stroma_compartments_report,
load_histopathological_tumor_nuclear_morphometry_report,
load_clinical_report,
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
search_pubmed,
query_medgemma,
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
        seed_genetic_algorithm, # cache analysis tool
        # spatial transcriptomics heatmap tools (cell type  / gene expression specific)
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
        # clinical report
        load_clinical_report,
        # helper tools
        search_pubmed,
        query_medgemma,
        # final answer tool
        final_answer_tool,
        ],
    max_steps=10,
)
# %%

if __name__ == "__main__":
    result = coding_agent.run("First, call seed_genetic_algorithm to understand what tools are most useful in describing the patients. Based on the previous results so far, describe the patient MW_B_001 and predict their prognosis. Very important : use <code></code> tags and not 'python' or 'tool code' or any other format")
    print(result) 
# %%
