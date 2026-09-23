export type AgentRole = 'Manager' | 'Researcher' | 'QA';
export type MessageType = 'task_update' | 'agent_message' | 'system' | 'error';

export interface Agent {
  name: string;
  role: AgentRole;
  status: 'idle' | 'thinking' | 'writing';
}

export interface Message {
  id: string;
  from_agent: string;
  to_agent: string;
  content: string;
  timestamp: string;
  message_type: MessageType;
}

export interface Task {
  id: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  conversation_log: Message[];
}
