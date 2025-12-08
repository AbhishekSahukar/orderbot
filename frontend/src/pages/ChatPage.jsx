import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./index.css"; // ✅ make sure only index.css is imported

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // ✅ Scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat/query", {
        query: input,
      });
      const botReply = res.data.answer || "⚠️ No response from server.";
      setMessages([...newMessages, { sender: "assistant", text: botReply }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { sender: "assistant", text: "⚠️ Error connecting to backend." },
      ]);
    }

    setInput(""); // ✅ clears input box after sending
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h2 className="chat-title">OrderBot Assistant</h2>

        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${
                msg.sender === "user" ? "user" : "assistant"
              }`}
            >
              {msg.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
