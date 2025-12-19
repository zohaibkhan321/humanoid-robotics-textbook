import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './Chatbot.css';

const Chatbot = ({ backendUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your Humanoid Robotics Textbook assistant. Ask me anything about humanoid robotics, and I\'ll find the relevant information for you.'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API
      const response = await fetch(`${backendUrl}/api/v1/answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query_text: inputValue,
          user_context: {}
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add bot response with citations
      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer || 'I couldn\'t generate a response. Please try rephrasing your question.',
        citations: data.citations || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting response:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setShowChat(!showChat);
    if (!showChat && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <div className="rag-chatbot">
      {showChat ? (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>🤖 Humanoid Robotics Assistant</h3>
            <button
              className="chatbot-close-btn"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`message message--${msg.role}`}
              >
                <div className="message-content">
                  {msg.content}
                </div>

                {msg.citations && msg.citations.length > 0 && (
                  <div className="message-citations">
                    <h4 className="citations-title">Sources:</h4>
                    <ul className="citations-list">
                      {msg.citations.map((cite, idx) => (
                        <li key={idx} className="citation-item">
                          <a
                            href={cite.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="citation-link"
                          >
                            {cite.text_preview ? cite.text_preview.substring(0, 100) + '...' : cite.url}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {msg.error && (
                  <div className="error-message">
                    <p>Please make sure the backend service is running at {backendUrl}</p>
                    <p>Start it with: <code>cd backend && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000</code></p>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="message message--assistant">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chatbot-input-form">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about humanoid robotics..."
              disabled={isLoading}
              className="chatbot-input"
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="chatbot-send-btn"
              aria-label="Send message"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
          </form>
        </div>
      ) : (
        <button
          className="chatbot-float-btn"
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16L14.5 18.5C14.1667 18.8333 13.75 19 13 19H6C4.61 19 3.42 18.26 2.71 17.19C2 16.12 2 14.8 2 13V7C2 5.61 2.74 4.42 3.81 3.71C4.88 3 6.1 3 7 3H17C17.5304 3 18.0391 3.21071 18.4142 3.58579C18.7893 3.96086 19 4.46957 19 5V15Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      )}
    </div>
  );
};

export default Chatbot;