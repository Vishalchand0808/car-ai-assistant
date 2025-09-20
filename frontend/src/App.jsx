// src/App.jsx

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios'; // Import axios

function App() {
  const [messages, setMessages] = useState([
    { sender: 'assistant', text: "Hello! I'm your in-car assistant. How can I help you?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // --- UPDATED: Function to connect to our FastAPI backend ---
  const sendMessageToBackend = async (text) => {
    // The backend server will be running on http://localhost:8000
    const API_URL = "https://huggingface.co/spaces/Vishalchand0808/car-ai-backend/process-command";
    
    try {
      const response = await axios.post(API_URL, {
        text: text, // Send the user's text in the request body
      });
      // Return the response text from the backend
      return response.data.response;
    } catch (error) {
      console.error("Error connecting to the backend:", error);
      // Return a user-friendly error message
      return "Sorry, I'm having trouble connecting to my brain right now.";
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const assistantResponseText = await sendMessageToBackend(input);
    const assistantMessage = { sender: 'assistant', text: assistantResponseText };
    
    setMessages(prev => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🚗 Car AI Assistant</h1>
        <p>Your smart driving companion</p>
      </header>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <p className="loading-dots">
              <span>.</span><span>.</span><span>.</span>
            </p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="input-form" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me to play music, get weather..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
