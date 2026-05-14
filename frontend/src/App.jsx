import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./index.css";

const API_BASE = import.meta.env.VITE_API_URL || "";


export default function App() {
  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "👋 Hi! I'm OrderBot. Ask me about any order — by customer name, product, or status.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const sendMessage = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const updated = [...messages, { sender: "user", text: trimmed }];
    setMessages(updated);
    setInput("");
    setIsThinking(true);

    try {
      const response = await axios.post(`${API_BASE}/api/chat/query`, {
        query: input,
      });
      setMessages([...updated, { sender: "assistant", text: data.answer || "No response." }]);
    } catch {
      setMessages([
        ...updated,
        { sender: "assistant", text: "⚠️ Could not reach the server. Please try again." },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h2 className="chat-title">OrderBot Assistant</h2>

        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}

          {isThinking && (
            <div className="chat-message assistant typing">
              OrderBot is thinking
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <form onSubmit={sendMessage} className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about an order..."
            disabled={isThinking}
          />
          <button type="submit" disabled={isThinking}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}