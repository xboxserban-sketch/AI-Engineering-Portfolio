import { useState } from 'react';
import { Agent } from '../types/swarm';

export function useSwarm() {
  const [agents, setAgents] = useState<Agent[]>([
    { name: 'Alice', role: 'Manager', status: 'idle' },
    { name: 'Bob', role: 'Researcher', status: 'idle' },
    { name: 'Charlie', role: 'QA', status: 'idle' }
  ]);
  const [status, setStatus] = useState<string>('idle');

  return { agents, setAgents, status, setStatus };
}
