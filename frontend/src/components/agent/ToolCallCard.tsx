import { CheckCircle2, Loader2, XCircle } from "lucide-react";
import type { ToolCall } from "../../types/agent";

const icon = {
  pending: <Loader2 size={12} className="animate-spin text-nexus-warn" />,
  success: <CheckCircle2 size={12} className="text-nexus-success" />,
  error: <XCircle size={12} className="text-nexus-danger" />,
};

export default function ToolCallCard({ call }: { call: ToolCall }) {
  return (
    <div className="rounded-lg border border-nexus-border/60 bg-nexus-panel p-2 text-xs">
      <div className="flex items-center gap-2">
        {icon[call.status]}
        <span className="font-mono text-nexus-accent">{call.name}</span>
      </div>
      <pre className="mt-1 overflow-x-auto whitespace-pre-wrap text-[10px] text-slate-400">
        {JSON.stringify(call.args, null, 2)}
      </pre>
      {call.result && (
        <pre className="mt-1 overflow-x-auto whitespace-pre-wrap text-[10px] text-nexus-success">
          → {JSON.stringify(call.result, null, 2)}
        </pre>
      )}
      {call.error && (
        <div className="mt-1 text-[10px] text-nexus-danger">{call.error}</div>
      )}
    </div>
  );
}
