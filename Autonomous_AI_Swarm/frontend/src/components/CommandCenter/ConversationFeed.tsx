import { Message } from '../../types/swarm';
import { motion } from 'framer-motion';

export function ConversationFeed({ messages }: { messages: Message[] }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 h-96 overflow-y-auto flex flex-col space-y-4">
      {messages.map((msg) => (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          key={msg.id} 
          className={`p-3 rounded-md ${msg.from_agent === 'System' ? 'bg-gray-800 text-gray-400 text-sm italic' : 'bg-gray-800 border-l-4 border-blue-500'}`}
        >
          <div className="flex justify-between items-center mb-1">
            <span className="font-bold text-blue-300">{msg.from_agent} &rarr; {msg.to_agent}</span>
            <span className="text-xs text-gray-500">{new Date(msg.timestamp).toLocaleTimeString()}</span>
          </div>
          <p className="text-gray-200">{msg.content}</p>
        </motion.div>
      ))}
    </div>
  );
}
