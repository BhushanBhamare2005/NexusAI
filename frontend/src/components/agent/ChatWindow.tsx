import { FormEvent, useState } from "react";
import ChatMessage from "./ChatMessage";
import { Button } from "../ui/button";
import type { AgentMessage } from "../../types/agent";

interface Props {
  messages: AgentMessage[];
  onSend: (text: string) => void;
  disabled?: boolean;
}

export default function ChatWindow({ messages, onSend, disabled }: Props) {
  const [text, setText] = useState("");

  const submit = (e: FormEvent) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <div className="flex h-full flex-col rounded-xl border border-nexus-border bg-nexus-panel">
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div className="text-sm text-nexus-muted">
            Ask NEXUS about a payment issue. Example:{" "}
            <span className="text-nexus-accent">
              "Maine ₹2,500 pay kiye, merchant ko nahi mila"
            </span>
          </div>
        )}
        {messages.map((m) => (
          <ChatMessage key={m.id} msg={m} />
        ))}
      </div>
      <form
        onSubmit={submit}
        className="flex gap-2 border-t border-nexus-border p-3"
      >
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe the issue…"
          className="flex-1 rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white outline-none focus:border-nexus-accent"
        />
        <Button type="submit" disabled={disabled}>
          Send
        </Button>
      </form>
    </div>
  );
}
