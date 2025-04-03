import React, { useState, useEffect, useRef } from 'react';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

interface ChatResponse {
  response: string;
  session_id: string;
}

const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Efecto para cargar el sessionId del localStorage al iniciar
  useEffect(() => {
    const savedSessionId = localStorage.getItem('chatSessionId');
    if (savedSessionId) {
      setSessionId(savedSessionId);
    }
  }, []);

  // Efecto para hacer scroll al último mensaje
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Función para formatear el texto con saltos de línea
  const formatMessageText = (text: string) => {
    return text.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line}
        {i < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch(import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: input,
          session_id: sessionId 
        }),
      });

      if (!response.ok) {
        throw new Error(`Error de servidor: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      
      // Guardar el sessionId para mantener la conversación
      if (data.session_id && data.session_id !== sessionId) {
        setSessionId(data.session_id);
        localStorage.setItem('chatSessionId', data.session_id);
      }

      const botMessage: Message = { 
        sender: 'bot', 
        text: data.response || 'No se recibió respuesta.' 
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error al contactar al agente:', error);
      setMessages(prev => [...prev, { 
        sender: 'bot', 
        text: '⚠️ Error al contactar al agente. Por favor, intenta de nuevo más tarde.' 
      }]);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-xl bg-white shadow-xl rounded-xl p-4 space-y-4">
      <div className="h-96 overflow-y-auto border rounded p-2 bg-gray-50 space-y-2">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 p-4">
            <p>👋 ¡Hola! Soy tu asistente de optimización de tráfico.</p>
            <p className="mt-2">Puedes pedirme que optimice parámetros como:</p>
            <ul className="mt-1 text-left list-disc pl-8">
              <li>Transporte público</li>
              <li>Congestión</li>
              <li>Emisiones</li>
              <li>Costo operacional</li>
            </ul>
            <p className="mt-2">Por ejemplo: "Quiero dar alta prioridad al transporte público y baja prioridad a las emisiones"</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg ${
                msg.sender === 'user' 
                  ? 'bg-blue-100 text-blue-900 self-end ml-auto' 
                  : 'bg-gray-200 text-gray-800 self-start mr-auto'
              } ${msg.sender === 'user' ? 'ml-12' : 'mr-12'} break-words`}
            >
              {formatMessageText(msg.text)}
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex items-center space-x-2 p-2">
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex space-x-2">
        <textarea
          className="flex-1 p-2 border rounded resize-none"
          rows={1}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe tu solicitud de optimización..."
          disabled={isLoading}
        />
        <button
          className={`px-4 py-2 rounded text-white ${
            isLoading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
          onClick={handleSend}
          disabled={isLoading}
        >
          Enviar
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
