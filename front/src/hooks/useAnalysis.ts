import { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:8000';

interface AnalysisRequest {
    case_id: string;
}

interface AnalysisResponse {
    task_id: string;
    status: string;
    message: string;
}

interface TaskStatus {
    task_id: string;
    status: string;
    case_id: string;
    created_at: string;
    completed_at?: string;
    result?: string;
    error?: string;
}

export const useAnalysis = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [taskId, setTaskId] = useState<string | null>(null);
    const [taskStatus, setTaskStatus] = useState<TaskStatus | null>(null);

    const startAnalysis = async (caseId: string) => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_BASE_URL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ case_id: caseId } as AnalysisRequest),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: AnalysisResponse = await response.json();
            setTaskId(data.task_id);
            return data;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
            setError(errorMessage);
            throw err;
        } finally {
            setIsLoading(false);
        }
    };

    const getTaskStatus = async (taskId: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/analyze/${taskId}/status`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: TaskStatus = await response.json();
            setTaskStatus(data);
            return data;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
            setError(errorMessage);
            throw err;
        }
    };

    const pollTaskStatus = (taskId: string, onComplete?: (result: TaskStatus) => void) => {
        const poll = async () => {
            try {
                const status = await getTaskStatus(taskId);

                if (status.status === 'completed' || status.status === 'failed') {
                    if (onComplete) {
                        onComplete(status);
                    }
                    return;
                }

                // Continue polling if still running
                setTimeout(() => poll(), 2000); // Poll every 2 seconds
            } catch (err) {
                console.error('Error polling task status:', err);
            }
        };

        poll();
    };

    const getAvailableCases = async (): Promise<string[]> => {
        try {
            const response = await fetch(`${API_BASE_URL}/cases`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
            setError(errorMessage);
            return [];
        }
    };

    return {
        isLoading,
        error,
        taskId,
        taskStatus,
        startAnalysis,
        getTaskStatus,
        pollTaskStatus,
        getAvailableCases,
    };
}; 