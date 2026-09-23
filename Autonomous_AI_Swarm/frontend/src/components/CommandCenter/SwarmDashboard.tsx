import { AgentCard } from './AgentCard';
import { ConversationFeed } from './ConversationFeed';
import { TaskInput } from './TaskInput';
import { StatusBar } from './StatusBar';
import { useWebSocket } from '../../hooks/useWebSocket';
import { useSwarm } from '../../hooks/useSwarm';
import { submitTask } from '../../services/api';

export function SwarmDashboard() {
  const { messages } = useWebSocket('ws://localhost:8000/ws');
  const { agents, status, setStatus } = useSwarm();

  const handleTaskSubmit = async (task: string) => {
    setStatus('in_progress');
    await submitTask(task);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <TaskInput onSubmit={handleTaskSubmit} />
      <div className="grid grid-cols-3 gap-6 mb-6">
        {agents.map(agent => (
          <AgentCard key={agent.name} agent={agent} />
        ))}
      </div>
      <ConversationFeed messages={messages} />
      <StatusBar status={status} />
    </div>
  );
}
