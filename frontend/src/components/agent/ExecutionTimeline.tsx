import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";
import { STEP_LABELS } from "../../lib/constants";
import type { AgentStep } from "../../types/agent";

const icons = {
  pending: <Circle size={14} className="text-nexus-muted" />,
  running: <Loader2 size={14} className="animate-spin text-nexus-accent" />,
  done: <CheckCircle2 size={14} className="text-nexus-success" />,
  failed: <XCircle size={14} className="text-nexus-danger" />,
  skipped: <Circle size={14} className="text-nexus-muted opacity-40" />,
};

export default function ExecutionTimeline({ steps }: { steps: AgentStep[] }) {
  return (
    <div className="space-y-2">
      {STEP_LABELS.map((label, i) => {
        const step = steps.find((s) => s.step === i + 1) || {
          step: i + 1,
          name: label,
          status: "pending" as const,
        };
        return (
          <div
            key={i}
            className={`flex items-start gap-3 rounded-lg border p-2 ${
              step.status === "running"
                ? "border-nexus-accent/50 bg-nexus-accent/5"
                : "border-nexus-border/60"
            }`}
          >
            <div className="mt-0.5">{icons[step.status]}</div>
            <div className="flex-1">
              <div className="text-sm text-white">
                {i + 1}. {label}
              </div>
              {step.detail && (
                <div className="text-[11px] text-nexus-muted">
                  {step.detail}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
