# API Integration Guide

This document explains how the frontend and backend are integrated for the GDM Hackathon project.

## Architecture

- **Backend**: FastAPI server (`api.py`) that wraps the `smolagent_coding_agent.py` function
- **Frontend**: React/Vite app that calls the API to trigger analyses and display results

## Quick Start

### 1. Install Dependencies

```bash
# Backend dependencies
uv sync

# Frontend dependencies (in front/ directory)
cd front
npm install
```

### 2. Run the Application

#### Option A: Run Backend Only
```bash
python run_dev.py
# or
python api.py
```

#### Option B: Run Frontend Only
```bash
cd front
npm run dev
```

#### Option C: Run Both (in separate terminals)
```bash
# Terminal 1 - Backend
python run_dev.py backend

# Terminal 2 - Frontend  
cd front && npm run dev
```

## API Endpoints

### POST /analyze
Start a new analysis for a case.

**Request:**
```json
{
  "case_id": "Case 001 - Lung Adenocarcinoma"
}
```

**Response:**
```json
{
  "task_id": "abc123-def456",
  "status": "pending",
  "message": "Analysis started for case Case 001 - Lung Adenocarcinoma"
}
```

### GET /analyze/{task_id}/status
Get the status of an analysis task.

**Response:**
```json
{
  "task_id": "abc123-def456",
  "status": "completed",
  "case_id": "Case 001 - Lung Adenocarcinoma",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:35:00",
  "result": "Analysis results from smolagent_coding_agent...",
  "error": null
}
```

### GET /cases
Get list of available cases.

**Response:**
```json
[
  "Case 001 - Lung Adenocarcinoma",
  "Case 002 - Breast Cancer IDC",
  "Case 003 - Prostate Adenocarcinoma"
]
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Frontend Integration

The frontend uses a custom hook (`useAnalysis`) to interact with the API:

```typescript
import { useAnalysis } from '@/hooks/useAnalysis';

const { startAnalysis, pollTaskStatus, getAvailableCases } = useAnalysis();

// Start analysis
const response = await startAnalysis(caseId);

// Poll for results
pollTaskStatus(response.task_id, (finalStatus) => {
  if (finalStatus.status === 'completed') {
    // Handle completed analysis
    console.log(finalStatus.result);
  }
});
```

## Development

### Backend Development
- The API runs on `http://localhost:8000`
- API documentation available at `http://localhost:8000/docs`
- The backend wraps the existing `run_coding_agent()` function from `smolagent_coding_agent.py`

### Frontend Development
- The frontend runs on `http://localhost:5173`
- Uses React Query for API state management
- Polls the backend every 2 seconds for status updates

### CORS Configuration
The backend is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative dev server)

## Troubleshooting

### Backend Issues
1. **Dependencies not installed**: Run `uv sync`
2. **Port already in use**: Change port in `api.py` or kill existing process
3. **Import errors**: Ensure all Python dependencies are installed

### Frontend Issues
1. **API connection failed**: Ensure backend is running on port 8000
2. **CORS errors**: Check CORS configuration in `api.py`
3. **Dependencies not installed**: Run `npm install` in `front/` directory

### Integration Issues
1. **Analysis not starting**: Check browser console for API errors
2. **Results not showing**: Verify polling is working and task completes successfully
3. **Status not updating**: Check network tab for failed API calls

## Production Deployment

For production, consider:
- Using a proper database instead of in-memory storage
- Adding authentication and rate limiting
- Using a task queue (Celery, RQ) for long-running analyses
- Setting up proper CORS for production domains
- Adding logging and monitoring 