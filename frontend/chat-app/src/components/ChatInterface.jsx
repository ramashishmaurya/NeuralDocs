import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, FileText } from 'lucide-react';

const ChatInterface = ({ currentFile }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Hello! Please upload a document from the sidebar to start asking questions about it.'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (currentFile && messages.length === 1) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: `I have successfully analyzed "${currentFile.name}". What would you like to know about this document?`
      }]);
    }
  }, [currentFile]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    
    if (!currentFile) {
      alert('Please upload a document first before asking questions.');
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate backend response
    setTimeout(() => {
      setIsTyping(false);
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: `This is a simulated answer for your question: "${userMessage.content}". Once the backend is connected, this will be replaced with real insights from your document.`
      };
      setMessages(prev => [...prev, botResponse]);
    }, 2000);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <main className="chat-container">
      <div className="messages-area">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.type}`}>
            <div className="avatar">
              {msg.type === 'user' ? <User size={20} /> : <Bot size={20} color="var(--accent-primary)" />}
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message-wrapper bot">
            <div className="avatar">
              <Bot size={20} color="var(--accent-primary)" />
            </div>
            <div className="message-content" style={{ padding: '12px 16px' }}>
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <form className="input-box" onSubmit={handleSendMessage}>
          <textarea
            className="chat-input"
            placeholder={currentFile ? "Ask a question about your document..." : "Upload a document to start chatting..."}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={!currentFile}
          />
          <button 
            type="submit" 
            className="send-button" 
            disabled={!inputValue.trim() || !currentFile}
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </main>
  );
};

export default ChatInterface;
