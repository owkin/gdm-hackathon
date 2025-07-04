# Heatmap Report Generation Tool

This tool provides functionality to analyze medical heatmap images using the gemma-3-27b multimodal model and save detailed descriptions to Google Cloud Storage.

## Overview

The heatmap report generation script is designed to:

1. **Load heatmap images** from Google Cloud Storage bucket for specific patient/feature combinations
2. **Analyze images** using the gemma-3-27b multimodal model to generate detailed descriptions
3. **Save descriptions** back to the bucket in JSON format with metadata

Then the tool can be used to load the reports from the bucket and use them in a smolagents agent.

## File Structure

```
gdm_hackathon/tools/heatmap_report/
├── generate_reports.py      # Report generation script
├── heatmap_tool.py          # Heatmap tools
├── test_tool.py             # Test suite
└── README.md               # This documentation
```
