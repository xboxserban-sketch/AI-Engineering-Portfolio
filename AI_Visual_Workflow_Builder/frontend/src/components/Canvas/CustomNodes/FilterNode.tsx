import React from 'react';
import { Handle, Position } from 'reactflow';

export const FilterNode = ({ data }: any) => {
    return (
        <div style={{ background: '#fef08a', padding: '10px', borderRadius: '5px', border: '1px solid #eab308' }}>
            <Handle type="target" position={Position.Top} />
            <div><strong>Filter</strong></div>
            <div style={{ fontSize: '12px' }}>{data?.status || 'PENDING'}</div>
            <Handle type="source" position={Position.Bottom} />
        </div>
    );
};
