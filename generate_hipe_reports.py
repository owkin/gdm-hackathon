"""A proof-of-concept for an agent that can write code using the Histowmics Toolbox
to analyze a WSI in natural language.

Improvements
------------
- Plot top tiles when using tile-level histomics.
- Make the agent write its own histomics function instead of relying on an existing one.
- Support the analysis of a cohort using histomics (creating top tiles plots and statistics plot = violin plots)
"""
import os
import math
from functools import lru_cache
from dotenv import load_dotenv
import openslide
from openslide.deepzoom import DeepZoomGenerator
import matplotlib.pyplot as plt
from smolagents import CodeAgent, LiteLLMRouterModel, tool, ToolCallingAgent
from sagemaker_toolbox.utils import Path
from histowmics.features.registry import HistomicsRegistry
from histowmics.helpers.data.io import read_slide_segmentation_data, SlideSegmentationData

CELL_MASKS_PATHS = "s3://abstra-project-storage-lttemftb/b96b040b-4f1c-4b75-b14a-43143c33b2c8/tcga_extraction/cell_masks/TCGA_BLCA/v6/"

SLIDE_DATA_PATH = ""
OUTPUT_DIR = "/home/sagemaker-user/user-default-efs/hipe_reports"

load_dotenv()


@lru_cache(maxsize=1)
def get_slide_data() -> SlideSegmentationData:
    """Get the slide data."""
    return read_slide_segmentation_data(SLIDE_DATA_PATH)


@lru_cache(maxsize=1)
def get_registry() -> HistomicsRegistry:
    """Get the registry of histomics functions."""
    return HistomicsRegistry.get_registry()


@tool
def get_available_cell_types() -> str:
    """
    Get the list of cell types, available to compute histomics from.

    Returns:
        str: The concatenated list of cell types separated by a comma.
    """
    slide_data = get_slide_data()
    return ",".join(slide_data.unique_cell_types)


@tool
def get_list_of_histomics_functions() -> str:
    """
    Get the list of histomics functions implemented in the Histowmics Toolbox.

    Returns:
        out: The list of available functions, separated by type of histomics (slide, tile, cell).
    """
    def _print_list_of_histomics_functions(fnames, family_name):
        registry = get_registry()
        out = f"List of {family_name} functions:\n"
        for fname in fnames:
            out += f"- {fname}\n"
            out += f"{registry[fname].__doc__}"
            out += "\n\n"
        return out
    out = _print_list_of_histomics_functions(
        HistomicsRegistry.get_slide_level_registry(), "Slide level histomics")
    return out


@tool
def histomics_function_executor(
    function_name: str,
    parameters: dict | None = None
) -> str:
    """
    Execute a histomics function and return its result.

    Args:
    function_name : Exact name under which the function is registered (see `get_list_of_histomics_functions`).
    parameters : Keyword arguments to forward to that function, *after*
        the slide data. Example::
            {"restrict_to_cell_types": ["tumor", "lymphocyte"]}

    Returns:
    str
        The DataFrame produced by the histomics function formatted as a string.
    """
    parameters = parameters or {}

    slide_data = get_slide_data()
    func = get_registry()[function_name]

    df = func(slide_data, **parameters)
    return df.to_string()


def get_agent_prompt(user_prompt: str) -> str:
    _AGENT_PROMPT = f"""
    You must analyze the current whole-slide image (WSI) and report insightful, trustworthy findings to the user.

    <rules>
    1. You are given a list of histomics function you must use to answer the user's question.
    2. All numerical or tabular results must originate from calls to the histomics function.
    3. After gathering the required information, write a clear, user-friendly answer that cites key figures and interpretations (omit long raw DataFrames unless very small).
    </rules>

    <question>
    {user_prompt}
    </question>
    """

    return _AGENT_PROMPT


def generate_report_for_slide(local_path: str, model) -> str:
    """Generate immune‑infiltration description for the given slide."""
    global SLIDE_DATA_PATH
    SLIDE_DATA_PATH = local_path
    get_slide_data.cache_clear()  # reset cached slide

    agent = ToolCallingAgent(
        tools=[
            get_list_of_histomics_functions,
            get_available_cell_types,
            histomics_function_executor,
        ],
        model=model,
    )

    agent_prompt = get_agent_prompt("Describe the immune infiltration.")
    return agent.run(agent_prompt)


def main() -> None:
    """Main function."""
    model = LiteLLMRouterModel(
        model_id="bedrock",
        model_list=[
            {
                "model_name": "bedrock",
                "litellm_params": {
                    "model": "bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
                    "aws_region_name": "eu-west-1",
                    "aws_access_key_id": os.getenv("K_AWS_ACCESS_KEY_ID"),
                    "aws_secret_access_key": os.getenv("K_AWS_SECRET_ACCESS_KEY"),
                    "aws_session_token": os.getenv("K_AWS_SESSION_TOKEN"),
                }
            }
        ]
    )

    cell_masks_paths = list(Path(CELL_MASKS_PATHS).glob("*/cell_masks.bin"))

    for cell_mask_path in cell_masks_paths:
        try:
            report = generate_report_for_slide(cell_mask_path, model)
        except Exception as exc:
            print(f"   ✗ Failed to process {cell_mask_path}: {exc}")
            continue

        report_path = Path(OUTPUT_DIR) / f"{cell_mask_path.parents[0].stem}.txt"
        report_path.write_text(report)
        print(f"   ✓ Saved → {report_path}")


if __name__ == "__main__":
    main()