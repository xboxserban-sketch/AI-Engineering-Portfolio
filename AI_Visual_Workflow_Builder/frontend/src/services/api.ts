import axios from 'axios';
import { Workflow, ExecutionResult } from '../types/workflow';

const API_URL = 'http://localhost:8000/api/v1';

export const api = {
    createWorkflow: async (workflow: Workflow): Promise<Workflow> => {
        const response = await axios.post(`${API_URL}/workflows/`, workflow);
        return response.data;
    },
    getWorkflows: async (): Promise<Workflow[]> => {
        const response = await axios.get(`${API_URL}/workflows/`);
        return response.data;
    },
    getWorkflow: async (id: string): Promise<Workflow> => {
        const response = await axios.get(`${API_URL}/workflows/${id}`);
        return response.data;
    },
    executeWorkflow: async (id: string): Promise<ExecutionResult> => {
        const response = await axios.post(`${API_URL}/workflows/${id}/execute`);
        return response.data;
    }
};
