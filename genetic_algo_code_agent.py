#!/usr/bin/env python3
"""
Genetic Algorithm Code Agent for Biomarker Discovery

This module implements an evolutionary optimization approach to discover
the best combination of medical reports for predicting patient survival.
It uses a genetic algorithm with evaluation tools to evolve optimal
biomarker combinations.
"""
# %%

# Standard library imports
from typing import List, Tuple

# Third-party imports
from smolagents import CodeAgent, FinalAnswerTool

# Local imports
from gdm_hackathon.models.vertex_models import get_model
from gdm_hackathon.tools.evaluation_tool import (
    evaluate_report_relevance_in_zero_shot,
    seed_genetic_algorithm,
)

# Import all available report tools
from gdm_hackathon.tools import (
    # Histopathological reports
    load_histopathological_immune_infiltration_report,
    load_histopathological_tumor_stroma_compartments_report,
    load_histopathological_tumor_nuclear_morphometry_report,
    
    # Clinical reports
    load_clinical_report,
    
    # Spatial transcriptomics heatmap reports
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
    
    # Genomic reports
    load_snv_indel_genomic_report,
    load_cnv_genomic_report,
    load_cna_genomic_report,
    load_gii_genomic_report,
    load_tmb_genomic_report,
    
    # Pathway reports
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
    
    # Helper tools
    search_pubmed,
    query_medgemma,
)


# Initialize the final answer tool
final_answer_tool = FinalAnswerTool()


def create_coding_agent() -> CodeAgent:
    """
    Create and configure the coding agent for evolutionary optimization.
    
    Returns:
        CodeAgent: Configured agent with all necessary tools and parameters.
    """
    # Initialize the model
    model = get_model("gemma-3-27b")
    
    # Define available tools for the agent
    available_tools = [
        # Core evaluation tools
        evaluate_report_relevance_in_zero_shot,
        seed_genetic_algorithm,

        # Histopathological reports
        load_histopathological_immune_infiltration_report,
        load_histopathological_tumor_stroma_compartments_report,
        load_histopathological_tumor_nuclear_morphometry_report,
        
        # Spatial transcriptomics heatmap reports
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
        
        # Genomic reports
        load_snv_indel_genomic_report,
        load_cnv_genomic_report,
        load_cna_genomic_report,
        load_gii_genomic_report,
        load_tmb_genomic_report,
        
        # Pathway reports (currently active)
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
        
        # Clinical reports
        load_clinical_report,
        
        # Helper tools
        search_pubmed,
        query_medgemma,
        
        # Final answer tool
        final_answer_tool,
    ]
    
    # Note: The following tools are commented out but available for future use
    # Spatial transcriptomics heatmap tools (cell type / gene expression specific)
    # Histopathological report family
    # Genomic report family
    
    return CodeAgent(
        model=model,
        name="coding_agent",
        description="A coding agent that selects the best 2 tools out of 3 available tools.",
        tools=available_tools,
        max_steps=50,  # Increased from 20 to 50 for more thorough optimization
    )


def get_optimization_prompt() -> str:
    """
    Get the comprehensive prompt for the evolutionary optimization task.
    
    Returns:
        str: The formatted prompt for the genetic algorithm optimization.
    """
    return r"""
# AI Agent Prompt: Evolutionary Optimization for Biomarker Discovery

You are a biomedical AI researcher running an **evolutionary optimization** to discover the best combination of medical reports for predicting patient survival. Your goal is to intelligently evolve solutions based on deep analysis of evaluation results.

## 🚀 MANDATORY FIRST STEP: Understand Current Progress

**BEFORE starting any optimization, you MUST first call `seed_genetic_algorithm()` to understand what has already been evaluated and learn from previous results.**

After reviewing the cache, you may optionally use:
- `search_pubmed()` to research relevant biomedical literature
- `query_medgemma()` to get insights about specific tools or combinations

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

* **Pair 1**: `("load_clinical_report", "load_fgfr3_pathway_report")` -> **Accuracy: 65%**, Balanced (FP: 3, FN: 2).
* **Pair 2**: `("load_histopathological_immune_infiltration_report", "load_cdk12_heatmap_report")` -> **Accuracy: 78%**, but Unbalanced (FP: 1, **FN: 6**).
* **Pair 3**: `("load_tmb_genomic_report", "load_emt_pathway_report")` -> **Accuracy: 55%**, Unbalanced (**FP: 7**, FN: 1).

**Your Thought Process should look like this:**

Start of the example:

Thought: The results for Generation 1 are in.

**1. Analysis:**
* Pair 2 has the highest accuracy (78%), but the confusion matrix shows it is too pessimistic, with 6 False Negatives. The reasoning for these FNs likely shows that even with strong immune signals, the model defaults to "Below Median" because it's missing context on tumor aggressiveness.
* Pair 1 is less accurate (65%) but much more balanced. This is a stable, but weaker, candidate.
* Pair 3 performed poorly and was too optimistic. I will discard this one.

**2. Strategy for Generation 2:**
My goal is to improve upon the high accuracy of Pair 2 while fixing its pessimistic bias.

* **(Elitism)**: I will keep the best pair, `("load_histopathological_immune_infiltration_report", "load_cdk12_heatmap_report")`, in the next generation to ensure I don't lose my best result.
* **(Informed Mutation)**: My hypothesis is that Pair 2 needs tumor context to be less pessimistic. I will **mutate** it by swapping one component for a report on tumor characteristics. I'll test `("load_histopathological_immune_infiltration_report", "load_histopathological_grade_report")`. This tests if adding tumor grade can correct the False Negatives.
* **(Crossover)**: I will create a new pair by **crossing over** the best components from my top two pairs. `load_histopathological_immune_infiltration_report` was the strongest component from the most accurate pair, and `load_clinical_report` was from the most balanced pair. This leads to the new candidate: `("load_histopathological_immune_infiltration_report", "load_clinical_report")`.

**3. Plan for Generation 2 Evaluation:**

Based on my strategy, the new population of 3 Candidate Pairs is ready. I will now evaluate them.

**Generation 2 Evaluation Plan**

<code>
# Elite Pair (from previous generation)
print(evaluate_report_relevance_in_zero_shot(tool1_name="load_histopathological_immune_infiltration_report", tool2_name="load_cdk12_heatmap_report"))
# Mutated Pair
print(evaluate_report_relevance_in_zero_shot(tool1_name="load_histopathological_immune_infiltration_report", tool2_name="load_clinical_report"))
</code>

End of the example.

## Your First Output

Thought: I must first understand the current state of the optimization by calling `seed_genetic_algorithm()` to see what combinations have already been evaluated. This will help me learn from previous results and avoid repeating evaluations.

<code>
# MANDATORY FIRST STEP: Understand current progress
print(seed_genetic_algorithm())
</code>

Based on the cache analysis, I will then design my evolutionary optimization strategy and begin evaluating new combinations.

## End of example

Very important use <code> </code> tags and not python or tool code or any other format

Let's begin the optimization !
"""


def run_coding_agent():
    """
    Run the smolagent coding agent to find the best report combination for survival prediction.
    
    Returns:
        The response from the coding agent containing the optimization results.
    """
    # Create the coding agent
    coding_agent = create_coding_agent()
    
    # Run the optimization with the comprehensive prompt
    response = coding_agent.run(get_optimization_prompt())
    
    return response


def main():
    """Main function to execute the genetic algorithm optimization."""
    print("🚀 Starting Genetic Algorithm Optimization for Biomarker Discovery...")
    print("=" * 70)
    
    try:
        result = run_coding_agent()
        print("\n" + "=" * 70)
        print("✅ Optimization Complete!")
        print("=" * 70)
        print(result)
    except Exception as e:
        print(f"\n❌ Error during optimization: {e}")
        raise


# %%

if __name__ == "__main__":
    main() 
# %%
