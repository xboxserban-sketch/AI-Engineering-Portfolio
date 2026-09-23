export enum NodeType {
    LLM_ANALYZE = 'LLM_ANALYZE',
    FILTER = 'FILTER',
    TRANSFORM = 'TRANSFORM',
    NOTIFY = 'NOTIFY'
}

export enum ExecutionStatus {
    PENDING = 'PENDING',
    RUNNING = 'RUNNING',
    SUCCESS = 'SUCCESS',
    FAILED = 'FAILED'
}

export interface NodeConfig {
    prompt?: string;
    regex?: string;
    mapping?: Record<string, string>;
    target?: string;
}

export interface WorkflowNode {
    id: string;
    type: NodeType | string; // For react flow string compatibility
    position?: { x: number, y: number };
    data: {
        config: NodeConfig;
        status: ExecutionStatus;
        result?: any;
        error?: string;
        label?: string;
    };
}

export interface WorkflowEdge {
    id: string;
    source: string;
    target: string;
}

export interface Workflow {
    id: string;
    name: string;
    nodes: WorkflowNode[];
    edges: WorkflowEdge[];
}

export interface ExecutionResult {
    workflow_id: string;
    status: ExecutionStatus;
    node_results: Record<string, any>;
}
