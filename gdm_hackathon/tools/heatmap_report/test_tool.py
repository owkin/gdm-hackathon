#!/usr/bin/env python3
"""
Test script for the Heatmap Report Generation Tool
"""

# %%

from gdm_hackathon.tools.heatmap_report.heatmap_tool import (
    load_tp53_heatmap_report,
)
from gdm_hackathon.models.vertex_models import get_model
from smolagents import CodeAgent


def test_heatmap_report_tools():
    """Test the individual heatmap report tools."""
    print("\n" + "="*60)
    print("Testing individual heatmap report tools:")
    print("="*60)
    
    # Test TP53 heatmap report
    patient_id = "CH_B_030"
    feature = "TP53"
    result = load_tp53_heatmap_report(patient_id)
    print(result)

def test_with_vertex_ai_agent():
    """Test with Vertex AI model using CodeAgent."""
    print("\n" + "="*60)
    print("Testing with Vertex AI model using CodeAgent")
    print("="*60)
    
    try:
        # Create an agent with the HIPE report tool
        model = get_model("gemma-3-27b")
        agent = CodeAgent(
            tools=[load_tp53_heatmap_report],
            model=model,
            name="heatmap_report_agent"
        )

        # Use the agent to load a report
        result = agent.run("Describe the spatial distribution of TP53 gene expression levels for patient CH_B_030")
        print(f"Vertex AI agent result: {result}")
        
    except Exception as e:
        print(f"Error with Vertex AI agent: {e}")


# %%

if __name__ == "__main__":
    test_heatmap_report_tools() 
    test_with_vertex_ai_agent()

#
# %%
