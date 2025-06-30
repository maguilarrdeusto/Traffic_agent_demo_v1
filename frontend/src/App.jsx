import React, { useState } from 'react';
import './App.css';

// Simple service for FastAPI backend
const API_BASE_URL = 'http://localhost:8001';

class ChatService {
  async sendMessage(message, sessionId = null) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, session_id: sessionId }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Send message error:', error);
      throw error;
    }
  }
}

const chatService = new ChatService();

// Add this utility function
function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}

// Main Chat Component
function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "¡Hello! I am your Optimization Agent. I can help you with::\n• Standard traffic optimization\n• Dynamic traffic optimization\n\nPlease describe which traffic parameters you want to optimize and I will be glad to help you.",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(`session-${Date.now()}`);

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatService.sendMessage(inputMessage, sessionId);
      
      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resetChat = () => {
    setMessages([
      {
        id: 1,
        text: "Hello! I am your Deusto Optimization Agent. I can help you with:\n• Standard traffic optimization\n• Dynamic traffic optimization.\n\nPlease describe which traffic parameters you want to optimize and I will help you with the analysis.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="p-4" style={{ backgroundColor: '#181533' }}>
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-4xl font-extrabold text-white mr-4">Deusto.</span>
            <span className="flex items-center text-lg text-white font-bold">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-6 h-6 mr-2 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 3.866-3.582 7-8 7a8.96 8.96 0 01-4-.93L3 19l1.07-3.21A7.963 7.963 0 013 12c0-3.866 3.582-7 8-7s8 3.134 8 7z"
                />
              </svg>
              Agente de optimización
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <button className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded text-sm text-white font-bold">
              Conectado
            </button>
            <button
              onClick={resetChat}
              className="bg-yellow-400 hover:bg-yellow-500 px-4 py-2 rounded text-sm text-gray-900 font-bold"
              title="Reiniciar conversación"
            >
              Reiniciar chat
            </button>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 max-w-4xl mx-auto p-4">
        <div className="flex-1 bg-white rounded-lg shadow-sm border flex flex-col">
          {/* Chat Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4 custom-scrollbar">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={cn(
                    "w-full max-w-2xl lg:max-w-3xl",
                    "px-6 py-4 rounded-2xl",
                    "custom-scrollbar",
                    message.sender === 'user'
                      ? 'bg-blue-600 text-white text-base leading-relaxed'
                      : 'bg-gray-100 text-gray-800 text-base leading-relaxed'
                  )}
                  style={{ maxHeight: '30rem', overflowY: 'auto' }}
                >
                  {message.sender === 'bot' && (
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                        <span className="text-base">🚗</span>
                      </div>
                      <span className="font-medium text-lg">Agente de optimización</span>
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{message.text}</div>
                  <div className={`text-sm mt-2 ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                    {message.timestamp}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu consulta sobre optimización de tráfico..."
                className="flex-1 px-5 py-3 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
              <button
                onClick={sendMessage}
                disabled={loading || !inputMessage.trim()}
                className="bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white px-8 py-3 rounded-lg text-lg"
              >
                Enviar
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-2 text-center">
              This agent specializes in **standard optimization** and **dynamic optimization** of traffic.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Main App Component
function App() {
  return <ChatInterface />;
}

export default App;

