import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import all tools
from gdm_hackathon.tools import (
    load_b_cell_heatmap_report,
    load_cdk12_heatmap_report,
    load_dc_heatmap_report,
    load_egfr_heatmap_report,
    load_endothelial_heatmap_report,
    load_epithelial_heatmap_report,
    load_erbb2_heatmap_report,
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
    load_t_nk_heatmap_report,
    load_tp53_heatmap_report,
)
from gdm_hackathon.tools.hipe_report.hipe_tool import (
    load_histopathological_immune_infiltration_report,
    load_histopathological_tumor_nuclear_morphometry_report,
    load_histopathological_tumor_stroma_compartments_report,
)

# Import your existing function
from smolagent_coding_agent import run_coding_agent

app = FastAPI(title="GDM Hackathon API", version="1.0.0")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for tasks (in production, use a database)
tasks: Dict[str, Dict[str, Any]] = {}


class AnalysisRequest(BaseModel):
    case_id: str


class AnalysisResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatus(BaseModel):
    task_id: str
    status: str
    case_id: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None


class ToolRequest(BaseModel):
    patient_id: str


def run_analysis_task(task_id: str, case_id: str):
    """Run the analysis in a separate thread"""
    try:
        tasks[task_id]["status"] = "running"
        tasks[task_id]["started_at"] = datetime.now().isoformat()

        # Call your existing function with the case_id
        result = run_coding_agent(case_id=case_id)

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        tasks[task_id]["result"] = result

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        tasks[task_id]["error"] = str(e)


# Individual tool endpoints
@app.post("/tools/b_cell_heatmap")
async def get_b_cell_heatmap(request: ToolRequest):
    """Get B cell heatmap report for a patient"""
    try:
        result = load_b_cell_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "b_cell_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/cdk12_heatmap")
async def get_cdk12_heatmap(request: ToolRequest):
    """Get CDK12 heatmap report for a patient"""
    try:
        result = load_cdk12_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "cdk12_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/dc_heatmap")
async def get_dc_heatmap(request: ToolRequest):
    """Get DC heatmap report for a patient"""
    try:
        result = load_dc_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "dc_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/egfr_heatmap")
async def get_egfr_heatmap(request: ToolRequest):
    """Get EGFR heatmap report for a patient"""
    try:
        result = load_egfr_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "egfr_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/endothelial_heatmap")
async def get_endothelial_heatmap(request: ToolRequest):
    """Get endothelial heatmap report for a patient"""
    try:
        result = load_endothelial_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "endothelial_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/epithelial_heatmap")
async def get_epithelial_heatmap(request: ToolRequest):
    """Get epithelial heatmap report for a patient"""
    try:
        result = load_epithelial_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "epithelial_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/erbb2_heatmap")
async def get_erbb2_heatmap(request: ToolRequest):
    """Get ERBB2 heatmap report for a patient"""
    try:
        result = load_erbb2_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "erbb2_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/fgfr3_heatmap")
async def get_fgfr3_heatmap(request: ToolRequest):
    """Get FGFR3 heatmap report for a patient"""
    try:
        result = load_fgfr3_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "fgfr3_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/fibroblast_heatmap")
async def get_fibroblast_heatmap(request: ToolRequest):
    """Get fibroblast heatmap report for a patient"""
    try:
        result = load_fibroblast_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "fibroblast_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/granulocyte_heatmap")
async def get_granulocyte_heatmap(request: ToolRequest):
    """Get granulocyte heatmap report for a patient"""
    try:
        result = load_granulocyte_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "granulocyte_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/il1b_heatmap")
async def get_il1b_heatmap(request: ToolRequest):
    """Get IL1B heatmap report for a patient"""
    try:
        result = load_il1b_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "il1b_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/krt7_heatmap")
async def get_krt7_heatmap(request: ToolRequest):
    """Get KRT7 heatmap report for a patient"""
    try:
        result = load_krt7_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "krt7_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/malignant_bladder_heatmap")
async def get_malignant_bladder_heatmap(request: ToolRequest):
    """Get malignant bladder heatmap report for a patient"""
    try:
        result = load_malignant_bladder_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "malignant_bladder_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/mast_heatmap")
async def get_mast_heatmap(request: ToolRequest):
    """Get mast heatmap report for a patient"""
    try:
        result = load_mast_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "mast_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/momac_heatmap")
async def get_momac_heatmap(request: ToolRequest):
    """Get MOMAC heatmap report for a patient"""
    try:
        result = load_momac_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "momac_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/muscle_heatmap")
async def get_muscle_heatmap(request: ToolRequest):
    """Get muscle heatmap report for a patient"""
    try:
        result = load_muscle_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "muscle_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/other_heatmap")
async def get_other_heatmap(request: ToolRequest):
    """Get other heatmap report for a patient"""
    try:
        result = load_other_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "other_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/pik3ca_heatmap")
async def get_pik3ca_heatmap(request: ToolRequest):
    """Get PIK3CA heatmap report for a patient"""
    try:
        result = load_pik3ca_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "pik3ca_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/plasma_heatmap")
async def get_plasma_heatmap(request: ToolRequest):
    """Get plasma heatmap report for a patient"""
    try:
        result = load_plasma_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "plasma_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/rb1_heatmap")
async def get_rb1_heatmap(request: ToolRequest):
    """Get RB1 heatmap report for a patient"""
    try:
        result = load_rb1_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "rb1_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/s100a8_heatmap")
async def get_s100a8_heatmap(request: ToolRequest):
    """Get S100A8 heatmap report for a patient"""
    try:
        result = load_s100a8_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "s100a8_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/t_nk_heatmap")
async def get_t_nk_heatmap(request: ToolRequest):
    """Get T/NK heatmap report for a patient"""
    try:
        result = load_t_nk_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "t_nk_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/tp53_heatmap")
async def get_tp53_heatmap(request: ToolRequest):
    """Get TP53 heatmap report for a patient"""
    try:
        result = load_tp53_heatmap_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "tp53_heatmap",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Histopathological report endpoints
@app.post("/tools/histopathological_immune_infiltration")
async def get_histopathological_immune_infiltration(request: ToolRequest):
    """Get histopathological immune infiltration report for a patient"""
    try:
        result = load_histopathological_immune_infiltration_report(request.patient_id)
        return {
            "patient_id": request.patient_id,
            "tool": "histopathological_immune_infiltration",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/histopathological_tumor_nuclear_morphometry")
async def get_histopathological_tumor_nuclear_morphometry(request: ToolRequest):
    """Get histopathological tumor nuclear morphometry report for a patient"""
    try:
        result = load_histopathological_tumor_nuclear_morphometry_report(
            request.patient_id
        )
        return {
            "patient_id": request.patient_id,
            "tool": "histopathological_tumor_nuclear_morphometry",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/histopathological_tumor_stroma_compartments")
async def get_histopathological_tumor_stroma_compartments(request: ToolRequest):
    """Get histopathological tumor stroma compartments report for a patient"""
    try:
        result = load_histopathological_tumor_stroma_compartments_report(
            request.patient_id
        )
        return {
            "patient_id": request.patient_id,
            "tool": "histopathological_tumor_stroma_compartments",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Main analysis endpoints
@app.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest):
    """Start a new analysis for a case"""
    task_id = str(uuid.uuid4())

    # Initialize task
    tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "case_id": request.case_id,
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }

    # Run analysis in background thread
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(run_analysis_task, task_id, request.case_id)

    return AnalysisResponse(
        task_id=task_id,
        status="pending",
        message=f"Analysis started for case {request.case_id}",
    )


@app.get("/analyze/{task_id}/status", response_model=TaskStatus)
async def get_analysis_status(task_id: str):
    """Get the status of an analysis task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]
    return TaskStatus(**task)


@app.get("/cases")
async def get_available_cases():
    """Get list of available cases"""
    # Return case IDs that match what the tools expect
    return [
        "test_patient",  # Default test case
        "CH_B_030a",  # Real patient IDs from your data
        "CH_B_033a",
        "CH_B_037a",
        "CH_B_041a",
        "CH_B_046a",
        "CH_B_059a",
        "CH_B_062a",
        "CH_B_064a",
        "CH_B_068a",
        "CH_B_069a",
        "CH_B_073a",
        "CH_B_074a",
        "CH_B_075a",
        "CH_B_079a",
        "CH_B_087a",
    ]


@app.get("/tools")
async def get_available_tools():
    """Get list of all available tools"""
    return {
        "heatmap_tools": [
            "b_cell_heatmap",
            "cdk12_heatmap",
            "dc_heatmap",
            "egfr_heatmap",
            "endothelial_heatmap",
            "epithelial_heatmap",
            "erbb2_heatmap",
            "fgfr3_heatmap",
            "fibroblast_heatmap",
            "granulocyte_heatmap",
            "il1b_heatmap",
            "krt7_heatmap",
            "malignant_bladder_heatmap",
            "mast_heatmap",
            "momac_heatmap",
            "muscle_heatmap",
            "other_heatmap",
            "pik3ca_heatmap",
            "plasma_heatmap",
            "rb1_heatmap",
            "s100a8_heatmap",
            "t_nk_heatmap",
            "tp53_heatmap",
        ],
        "histopathological_tools": [
            "histopathological_immune_infiltration",
            "histopathological_tumor_nuclear_morphometry",
            "histopathological_tumor_stroma_compartments",
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
