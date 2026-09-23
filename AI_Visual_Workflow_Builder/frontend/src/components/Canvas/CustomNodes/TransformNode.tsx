import React from 'react';
import { Handle, Position } from 'reactflow';

export const TransformNode = ({ data }: any) => {
    return (
        <div style={{ background: '#d9f99d', padding: '10px', borderRadius: '5px', border: '1px solid #84cc16' }}>
            <Handle type="target" position={Position.Top} />
            <div><strong>Transform</strong></div>
            <div style={{ fontSize: '12px' }}>{data?.status || 'PENDING'}</div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
};
