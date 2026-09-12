import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your AI customer-support agent. Ask me about orders, refunds, cancellations, or delivery.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", text: userText }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userText,
          customer_id: "demo-user",
          history: messages.map((m) => ({
            role: m.role,
            content: m.text,
          })),
        }),
      });

      if (!response.ok) throw new Error("API request failed");
      const data = await response.json();

      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: data.response,
          meta: `${data.intent} • ${data.tool_result}`,
        },
      ]);
    } catch (error) {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: "I couldn't connect to the support server. Please check the backend URL.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>🤖 AI Support</h1>
        <p>Agentic Customer Support</p>

        <div className="features">
          <div>🧠 LangGraph Agent</div>
          <div>📚 RAG Knowledge</div>
          <div>🔧 Business Tools</div>
          <div>🗄️ PostgreSQL Ready</div>
        </div>
      </aside>

      <main className="chat">
        <header>
          <div>
            <h2>Customer Support</h2>
            <span>● AI Agent Online</span>
          </div>
        </header>

        <section className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="bubble">{message.text}</div>
              {message.meta && <small>{message.meta}</small>}
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="bubble">Thinking and checking tools...</div>
            </div>
          )}
        </section>

        <form className="input-area" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your order..."
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}
