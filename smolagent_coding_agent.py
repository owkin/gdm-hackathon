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
    # AI Agent Prompt: Evolutionary Optimization for Biomarker Discovery

You are a biomedical AI researcher running an **evolutionary optimization** to discover the best combination of medical reports for predicting patient survival. Your goal is to intelligently evolve solutions based on deep analysis of evaluation results.

## 🧬 Your Methodology: Evolutionary Optimization

You will find the best combination of 2 reports by evolving a **population** of candidate solutions over several **generations**.

* **Report/Component**: A single report-generating tool (e.g., `load_clinical_report`).
* **Candidate Pair**: A pair of two reports representing one candidate solution (e.g., `["load_clinical_report", "load_fgfr3_pathway_report"]`).
* **Fitness**: A score indicating how well a **Candidate Pair** predicts survival. A good fitness score means high accuracy AND a balanced model (low False Positives/Negatives).
* **Evolution**: Creating new, potentially better **Candidate Pairs** using techniques like **Crossover** (mixing reports from successful pairs) and **Mutation** (swapping one report to test a hypothesis).

---

## 🛠️ Available Tools & Evaluation

* **Report Tools**: You have access to Spatial, Histopathological, Clinical, Pathway, and Genomic report tools.
* **Evaluation Tool**: `evaluate_report_relevance_in_zero_shot(tool1_name: str, tool2_name: str)`. This is your fitness function. It returns a detailed report including accuracy, a confusion matrix, and reasoning for example predictions.

---

## 🧠 The Evolutionary Workflow (Your Task)

You have a budget of **~10 generations** (with a population size of 3-5 per generation).

1.  **Generation 1 (Initialization)**: Create an initial population of 3-4 diverse **Candidate Pairs**. Choose components from different families to broadly survey the landscape. Evaluate this entire population.

2.  **Analyze & Strategize (THE MOST IMPORTANT STEP)**: For each result in the generation, you must **look beyond the accuracy score**. Analyze the full evaluation output, especially the **Confusion Matrix** and the **Reasoning** for incorrect predictions (False Positives/Negatives).

3.  **Generation 2+ (Evolve)**: Based on your analysis, create the next generation's population using **Elitism**, **Crossover**, and **Informed Mutation**.

4.  **Repeat**: Repeat steps 2 and 3 for each generation, continuously refining your population of **Candidate Pairs**.

5.  **Final Recommendation**: Once you have a clear winner that is both accurate and balanced, use the `final_answer_tool` to submit your answer.

---

## 📝 Example of a Full Generation Cycle

This is what your thought process should look like after an evaluation.

**Situation**: You have just received the results for your 3 **Candidate Pairs** in Generation 1.

* **Pair 1**: `("clinical_report", "fgfr3_pathway_report")` -> **Accuracy: 65%**, Balanced (FP: 3, FN: 2).
* **Pair 2**: `("histopathological_immune_infiltration_report", "cd8_heatmap_report")` -> **Accuracy: 78%**, but Unbalanced (FP: 1, **FN: 6**).
* **Pair 3**: `("tp53_genomic_report", "emt_pathway_report")` -> **Accuracy: 55%**, Unbalanced (**FP: 7**, FN: 1).

**Your Thought Process should look like this:**

Start of the example:

Thought: The results for Generation 1 are in.

**1. Analysis:**
* Pair 2 (`histo_immune`, `cd8_heatmap`) has the highest accuracy (78%), but the confusion matrix shows it is too pessimistic, with 6 False Negatives. The reasoning for these FNs likely shows that even with strong immune signals, the model defaults to "Below Median" because it's missing context on tumor aggressiveness.
* Pair 1 (`clinical`, `fgfr3_pathway`) is less accurate (65%) but much more balanced. This is a stable, but weaker, candidate.
* Pair 3 (`tp53`, `emt`) performed poorly and was too optimistic. I will discard this one.

**2. Strategy for Generation 2:**
My goal is to improve upon the high accuracy of Pair 2 while fixing its pessimistic bias.

* **(Elitism)**: I will keep the best pair, `("histopathological_immune_infiltration_report", "cd8_heatmap_report")`, in the next generation to ensure I don't lose my best result.
* **(Informed Mutation)**: My hypothesis is that Pair 2 needs tumor context to be less pessimistic. I will **mutate** it by swapping one component for a report on tumor characteristics. I'll test `("histopathological_immune_infiltration_report", "histopathological_grade_report")`. This tests if adding tumor grade can correct the False Negatives.
* **(Crossover)**: I will create a new pair by **crossing over** the best components from my top two pairs. `histopathological_immune_infiltration_report` was the strongest component from the most accurate pair, and `clinical_report` was from the most balanced pair. This leads to the new candidate: `("histopathological_immune_infiltration_report", "clinical_report")`.

**3. Plan for Generation 2 Evaluation:**

Based on my strategy, the new population of 3 Candidate Pairs is ready. I will now evaluate them.

**Generation 2 Evaluation Plan**

<code>
# Elite Pair (from previous generation)
print(evaluate_report_relevance_in_zero_shot(tool1_name="histopathological_immune_infiltration_report", tool2_name="cd8_heatmap_report"))
# Mutated Pair
print(evaluate_report_relevance_in_zero_shot(tool1_name="histopathological_immune_infiltration_report", tool2_name="histopathological_grade_report"))
# Crossover Pair
print(evaluate_report_relevance_in_zero_shot(tool1_name="histopathological_immune_infiltration_report", tool2_name="clinical_report"))
</code>

End of the example.

## Your First Output

Thought: I will start my evolutionary optimization. For Generation 1, I need to create a diverse initial population. I will create a population of 3 **Candidate Pairs**, pairing a clinical report with a pathway report, a histopathology report with a spatial report, and a genomic report with another pathway report. Then I will evaluate them all.

<code>
# Generation 1 Evaluation Plan
print(evaluate_report_relevance_in_zero_shot(tool1_name="load_clinical_report", tool2_name="load_fgfr3_pathway_report"))
print(evaluate_report_relevance_in_zero_shot(tool1_name="load_histopathological_immune_infiltration_report", tool2_name="load_cnv_genomic_report"))
print(evaluate_report_relevance_in_zero_shot(tool1_name="load_egfr_pathway_report", tool2_name="load_tp53_heatmap_report"))
</code>

Let's begin the optimization, and don't forget to justify your reasoning for the final answer ! 
"""

    )
    return response

if __name__ == "__main__":
    result = run_coding_agent()
    print(result) 
# %%
