"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendMessage, resetSession } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const SUGGESTIONS = [
  "Why are you the right fit for this role?",
  "Tell me about the Patient Management System",
  "What's your experience with microservices?",
  "Walk me through your AI Study Planner project",
  "What tech stack are you most comfortable with?",
  "Can we schedule an interview?",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = useCallback(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  }, [input]);

  const handleSend = async (text?: string) => {
    const messageText = text || input.trim();
    if (!messageText || isLoading) return;

    setError(null);
    setInput("");

    // Add user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: messageText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(messageText, sessionId || undefined);

      // Store session ID
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      // Add AI response
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Something went wrong";
      setError(errorMessage);

      // Add error message as AI response
      const errorMsg: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: `⚠️ Sorry, I encountered an error: ${errorMessage}. Please make sure the backend server is running on port 8000.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleReset = async () => {
    if (sessionId) {
      await resetSession(sessionId).catch(() => {});
    }
    setMessages([]);
    setSessionId(null);
    setError(null);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="avatar">UB</div>
          <div className="header-info">
            <h1>Utkersh Basnet</h1>
            <div className="subtitle">
              <span className="status-dot"></span>
              AI Persona • Ready to chat
            </div>
          </div>
        </div>
        <div className="header-actions">
          <button
            className="btn-icon"
            onClick={handleReset}
            title="New conversation"
            aria-label="New conversation"
          >
            ↻
          </button>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="chat-container">
        {messages.length === 0 && (
          <div className="welcome-card">
            <div className="welcome-avatar">UB</div>
            <h2>Hey, I&apos;m Utkersh&apos;s AI 👋</h2>
            <p>
              I&apos;m Utkersh&apos;s AI representative. Ask me about his
              projects, tech stack, experience, or schedule an interview.
              Everything I say is grounded in his real resume and GitHub repos.
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`message-row ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === "assistant" ? "UB" : "You"}
            </div>
            <div className="message-bubble">
              {msg.role === "assistant" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="typing-indicator">
            <div className="message-avatar" style={{
              width: 32, height: 32, borderRadius: "50%",
              background: "linear-gradient(135deg, #7c3aed, #2563eb, #06b6d4)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 13, fontWeight: 600, color: "white", flexShrink: 0
            }}>
              UB
            </div>
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {!isLoading && (
          <div className="suggestion-chips">
            {SUGGESTIONS.map((suggestion, i) => (
              <button
                key={i}
                className="chip"
                onClick={() => handleSend(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            className="input-field"
            placeholder="Ask me anything about Utkersh..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            id="chat-input"
          />
          <button
            className="send-button"
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            aria-label="Send message"
            id="send-button"
          >
            ➤
          </button>
        </div>
        <p className="input-hint">
          RAG-grounded on real resume & GitHub • Press Enter to send, Shift+Enter for
          new line
        </p>
      </div>
    </div>
  );
}
