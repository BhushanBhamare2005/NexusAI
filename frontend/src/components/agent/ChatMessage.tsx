import type { AgentMessage } from "../../types/agent";
import { formatDate } from "../../lib/formatters";

export default function ChatMessage({ msg }: { msg: AgentMessage }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-xl px-3 py-2 text-sm ${
          isUser
            ? "bg-nexus-accent/20 text-white"
            : "bg-white/5 text-slate-200"
        }`}
      >
        <div className="whitespace-pre-wrap">{msg.content}</div>
        <div className="mt-1 text-[10px] text-nexus-muted">
          {formatDate(msg.timestamp)}
        </div>
      </div>
    </div>
  );
}
