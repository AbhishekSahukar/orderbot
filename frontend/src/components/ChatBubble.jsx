export default function ChatBubble({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`px-4 py-3 rounded-lg max-w-2xl leading-relaxed shadow-sm 
        ${isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"}`}
      >
        {text}
      </div>
    </div>
  );
}
