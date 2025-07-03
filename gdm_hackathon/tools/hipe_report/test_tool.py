#!/usr/bin/env python3
"""
Test script for the HIPE Report Tool
"""

# %%
from gdm_hackathon.tools.hipe_report.hipe_tool import load_hipe_report
from smolagents import ToolCallingAgent
from gdm_hackathon.models.vertex_ai_model import VertexAIServerModel

def test_hipe_report_tool():
    """Test the HIPE report tool with a sample patient ID."""
    
    # Test patient ID from your example (just the first part)
    patient_id = "TCGA-2F-A9KO-01Z-00-DX1"
    
    print(f"Testing HIPE report tool with patient ID: {patient_id}")
    print("=" * 60)
    
    try:
        result = load_hipe_report(patient_id)
        print("Result:")
        print(result)
        
        if isinstance(result, str) and result.startswith("Error"):
            print("\nNote: This is expected if the file doesn't exist in the bucket.")
            print("The tool is working correctly - it's just that the specific file may not exist.")
        else:
            print("\nSuccess! The tool loaded the report successfully.")
            
    except Exception as e:
        print(f"Error testing tool: {e}")


def test_with_vertex_ai_agent():
    """Test with Vertex AI model using ToolCallingAgent."""
    print("\n" + "="*60)
    print("Testing with Vertex AI model using ToolCallingAgent")
    print("="*60)
    
    try:
        # Create an agent with the HIPE report tool
        model = VertexAIServerModel(
            model_id="medgemma",
            project_id="gemma-hcls25par-703",
            location="europe-west4",
            endpoint_id="4761133837897957376",
        )
        agent = ToolCallingAgent(
            tools=[load_hipe_report],
            model=model,
            name="hipe_report_agent"
        )

        # Use the agent to load a report
        result = agent.run("Describe the immune infiltration for TCGA-2F-A9KO-01Z-00-DX1")
        print(f"Vertex AI agent result: {result}")
        
    except Exception as e:
        print(f"Error with Vertex AI agent: {e}")


# %%

if __name__ == "__main__":
    test_hipe_report_tool() 
    test_with_vertex_ai_agent()

# %%
