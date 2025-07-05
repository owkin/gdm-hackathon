import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
