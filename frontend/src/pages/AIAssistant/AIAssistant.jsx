import React, { useState, useRef, useEffect } from 'react';
import { chatWithAI } from '../../services/aiService';
import { getCurrentUser } from '../../services/authService';
import { Sparkles, Send } from 'lucide-react';
import styles from './AIAssistant.module.css';

const AIAssistant = () => {
  const user = getCurrentUser();
  const [messages, setMessages] = useState([
    { id: 1, type: 'ai', text: 'Hello! I am SmartCart AI, your personal grocery assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userText = input.trim();
    setInput('');
    
    // Add user message to UI
    const newUserMsg = { id: Date.now(), type: 'user', text: userText };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const response = await chatWithAI(user?.id || 'anonymous', userText);
      setMessages(prev => [...prev, { id: Date.now(), type: 'ai', text: response.message }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        type: 'error', 
        text: 'AI assistant is temporarily unavailable. Please try again later.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.aiPage}>
      <div className={styles.container}>
        
        <div className={styles.sidebar}>
          <div className={styles.aiBranding}>
            <div className={styles.iconCircle}>
              <Sparkles size={32} color="var(--primary-green)" />
            </div>
            <h1>SmartCart AI</h1>
            <p>Your personal grocery assistant.</p>
          </div>
          
          <div className={styles.suggestions}>
            <h3>Try asking:</h3>
            <div className={styles.suggestionList}>
              <button onClick={() => setInput("I need groceries for breakfast for 4 people")}>
                "I need groceries for breakfast for 4 people"
              </button>
              <button onClick={() => setInput("What are the best dairy products under 100 rupees?")}>
                "What are the best dairy products under 100 rupees?"
              </button>
              <button onClick={() => setInput("Help me plan a vegetarian dinner.")}>
                "Help me plan a vegetarian dinner."
              </button>
            </div>
          </div>
        </div>
        
        <div className={styles.chatArea}>
          <div className={styles.messagesContainer}>
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`${styles.messageWrapper} ${
                  msg.type === 'user' ? styles.wrapperUser : styles.wrapperAi
                }`}
              >
                <div className={`${styles.messageBubble} ${styles[`bubble${msg.type}`]}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className={`${styles.messageWrapper} ${styles.wrapperAi}`}>
                <div className={`${styles.messageBubble} ${styles.bubbleai} ${styles.typing}`}>
                  <span className={styles.dot}></span>
                  <span className={styles.dot}></span>
                  <span className={styles.dot}></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <form onSubmit={handleSend} className={styles.inputArea}>
            <input 
              type="text" 
              className={styles.input}
              placeholder="Ask something like: I need groceries for breakfast for 4 people"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" className={styles.sendBtn} disabled={!input.trim() || isLoading}>
              <Send size={20} />
            </button>
          </form>
        </div>
        
      </div>
    </div>
  );
};

export default AIAssistant;
