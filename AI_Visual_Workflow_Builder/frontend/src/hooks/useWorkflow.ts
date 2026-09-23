import { useState, useCallback } from 'react';
import { Node, Edge, addEdge, Connection, applyNodeChanges, NodeChange, applyEdgeChanges, EdgeChange } from 'reactflow';
import { api } from '../services/api';
import { Workflow, WorkflowNode, ExecutionStatus, NodeType } from '../types/workflow';

export const useWorkflow = () => {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const [workflowId, setWorkflowId] = useState<string>('test-wf-1');

    const onNodesChange = useCallback(
        (changes: NodeChange[]) => setNodes((nds) => applyNodeChanges(changes, nds)),
        []
    );
    const onEdgesChange = useCallback(
        (changes: EdgeChange[]) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        []
    );
    const onConnect = useCallback(
        (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
        []
    );

    const saveWorkflow = async () => {
        const wfNodes: WorkflowNode[] = nodes.map(n => ({
            id: n.id,
            type: n.type || NodeType.LLM_ANALYZE,
            data: {
                config: n.data?.config || {},
                status: ExecutionStatus.PENDING
            }
        }));
        const wfEdges = edges.map(e => ({ id: e.id, source: e.source, target: e.target }));
        
        const workflow: Workflow = {
            id: workflowId,
            name: 'My Workflow',
            nodes: wfNodes,
            edges: wfEdges
        };
        await api.createWorkflow(workflow);
        alert('Workflow saved!');
    };

    const executeWorkflow = async () => {
        try {
            const result = await api.executeWorkflow(workflowId);
            alert(`Execution finished with status: ${result.status}`);
        } catch (e) {
            alert('Execution failed');
        }
    };

    return {
        nodes, setNodes, edges, setEdges, onNodesChange, onEdgesChange, onConnect, saveWorkflow, executeWorkflow
    };
};
