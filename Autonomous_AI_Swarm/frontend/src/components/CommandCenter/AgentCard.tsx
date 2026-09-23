import { Agent } from '../../types/swarm';

export function AgentCard({ agent }: { agent: Agent }) {
  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-xl font-semibold text-white">{agent.name}</h3>
        <span className="px-2 py-1 bg-blue-900 text-blue-200 text-xs rounded-full">{agent.role}</span>
      </div>
      <div className="flex items-center space-x-2">
        <div className={`w-3 h-3 rounded-full ${agent.status === 'idle' ? 'bg-gray-500' : 'bg-green-500 animate-pulse'}`}></div>
        <span className="text-sm text-gray-400 capitalize">{agent.status}</span>
      </div>
    </div>
  );
}
