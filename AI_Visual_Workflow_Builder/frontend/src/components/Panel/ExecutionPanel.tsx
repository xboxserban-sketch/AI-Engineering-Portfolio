import React from 'react';

export const ExecutionPanel = () => {
    return (
        <div style={{ position: 'absolute', right: 10, top: 10, background: 'white', padding: 10, border: '1px solid #ccc', zIndex: 4 }}>
            <h3>Execution Status</h3>
            <p>Real-time monitoring</p>
        </div>
    );
};
