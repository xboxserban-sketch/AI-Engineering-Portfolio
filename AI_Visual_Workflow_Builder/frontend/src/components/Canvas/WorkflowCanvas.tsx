import React from 'react';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import { LLMNode } from './CustomNodes/LLMNode';
import { FilterNode } from './CustomNodes/FilterNode';
import { TransformNode } from './CustomNodes/TransformNode';
import { useWorkflow } from '../../hooks/useWorkflow';
import { ExecutionPanel } from '../Panel/ExecutionPanel';
import { NodeConfigPanel } from '../Panel/NodeConfigPanel';

const nodeTypes = {
    LLM_ANALYZE: LLMNode,
    FILTER: FilterNode,
    TRANSFORM: TransformNode
};

export const WorkflowCanvas = () => {
    const { nodes, edges, onNodesChange, onEdgesChange, onConnect, saveWorkflow, executeWorkflow, setNodes } = useWorkflow();

    const addNode = () => {
        const newNode = {
            id: `node-${nodes.length + 1}`,
            type: 'LLM_ANALYZE',
            position: { x: Math.random() * 200, y: Math.random() * 200 },
            data: { label: 'New Node', status: 'PENDING', config: {} }
        };
        setNodes([...nodes, newNode]);
    };

    return (
        <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
            <div style={{ position: 'absolute', zIndex: 4, margin: '10px' }}>
                <button onClick={addNode} style={{ marginRight: '10px' }}>Add LLM Node</button>
                <button onClick={saveWorkflow} style={{ marginRight: '10px' }}>Save Workflow</button>
                <button onClick={executeWorkflow}>Execute Workflow</button>
            </div>
            <ExecutionPanel />
            <NodeConfigPanel />
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                nodeTypes={nodeTypes}
            >
                <Background />
                <Controls />
            </ReactFlow>
        </div>
    );
};
