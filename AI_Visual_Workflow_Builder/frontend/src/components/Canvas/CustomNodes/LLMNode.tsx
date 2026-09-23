import React from 'react';
import { Handle, Position } from 'reactflow';

export const LLMNode = ({ data }: any) => {
    return (
        <div style={{ background: '#e0f2fe', padding: '10px', borderRadius: '5px', border: '1px solid #38bdf8' }}>
            <Handle type="target" position={Position.Top} />
            <div><strong>LLM Analyze</strong></div>
            <div style={{ fontSize: '12px' }}>{data?.status || 'PENDING'}</div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
};
