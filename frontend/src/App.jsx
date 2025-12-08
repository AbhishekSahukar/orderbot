import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./index.css";

const API_BASE = import.meta.env.VITE_API_URL;

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "👋 Hello! I'm OrderBot. I can help you check order statuses, customer orders, and delivery updates."
    }
  ]);

  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [
      ...messages,
      { sender: "user", text: input }
    ];
    setMessages(newMessages);
    setInput("");

    // SHOW thinking indicator
    setIsThinking(true);

    try {
      const response = await axios.post(`${API_BASE}/chat/query`, {
        query: input,
      });

      const answer = response.data.answer || "No response.";

      setMessages([
        ...newMessages,
        { sender: "assistant", text: answer }
      ]);
    } catch (error) {
      console.error("Backend error:", error);
      setMessages([
        ...newMessages,
        { sender: "assistant", text: "⚠️ Error connecting to backend." }
      ]);
    }

    // HIDE thinking indicator
    setIsThinking(false);
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h2 className="chat-title">OrderBot Assistant</h2>

        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${msg.sender === "user" ? "user" : "assistant"}`}
            >
              {msg.text}
            </div>
          ))}

          {/* Typing indicator */}
          {isThinking && (
            <div className="chat-message assistant typing">
              OrderBot is thinking…
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <form onSubmit={sendMessage} className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;
