import { useEffect, useRef, useState } from 'react';
import { Message } from '../types/swarm';

export function useWebSocket(url: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(url);
    ws.current.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setMessages(prev => [...prev, msg]);
    };
    return () => ws.current?.close();
  }, [url]);

  return { messages };
}
