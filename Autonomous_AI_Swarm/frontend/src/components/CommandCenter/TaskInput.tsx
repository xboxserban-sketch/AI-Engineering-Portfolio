import { useState } from 'react';

export function TaskInput({ onSubmit }: { onSubmit: (task: string) => void }) {
  const [task, setTask] = useState('');

  return (
    <div className="flex space-x-4 mb-6">
      <input 
        type="text" 
        className="flex-1 bg-gray-800 text-white border border-gray-700 rounded px-4 py-2 focus:outline-none focus:border-blue-500"
        placeholder="Enter a task to deploy the swarm..."
        value={task}
        onChange={(e) => setTask(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && onSubmit(task)}
      />
      <button 
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded transition-colors"
        onClick={() => onSubmit(task)}
      >
        Deploy Swarm
      </button>
    </div>
  );
}
