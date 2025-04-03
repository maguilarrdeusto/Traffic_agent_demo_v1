import React from 'react';
import Chatbot from './components/Chatbot';

const App = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">🚦 Traffic Optimization Chatbot</h1>
      <Chatbot />
    </div>
  );
};

export default App;
