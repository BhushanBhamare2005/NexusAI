import { Card } from "../ui/card";
import { Badge } from "../ui/badge";
import type { AgentRun } from "../../types/agent";

export default function ResolutionReceipt({ run }: { run: AgentRun }) {
  const tone =
    run.status === "resolved"
      ? "success"
      : run.status === "escalated"
      ? "danger"
      : run.status === "awaiting_approval"
      ? "warn"
      : "accent";

  return (
    <Card className="border-nexus-accent/30">
      <div className="flex items-center justify-between">
        <div className="text-xs uppercase tracking-wide text-nexus-muted">
          Resolution Receipt
        </div>
        <Badge tone={tone}>{run.status.replace("_", " ")}</Badge>
      </div>
      <div className="mt-2 text-xs">
        <span className="text-nexus-muted">Outcome verification:</span>{" "}
        <span className={run.verified ? "text-nexus-success" : "text-nexus-warn"}>
          {run.verified ? "verified" : "not verified"}
        </span>
      </div>
      <div className="mt-2 space-y-1 text-xs">
        <div>
          <span className="text-nexus-muted">Case:</span> {run.caseId}
        </div>
        {run.intent && (
          <div>
            <span className="text-nexus-muted">Intent:</span> {run.intent}
          </div>
        )}
        {run.rootCause && (
          <div>
            <span className="text-nexus-muted">Root cause:</span>{" "}
            {run.rootCause}
          </div>
        )}
        {run.selectedAction && (
          <div>
            <span className="text-nexus-muted">Action taken:</span>{" "}
            {run.selectedAction}
          </div>
        )}
        {run.riskLevel && (
          <div>
            <span className="text-nexus-muted">Risk level:</span>{" "}
            {run.riskLevel}
          </div>
        )}
      </div>
      {run.finalResponse && (
        <div className="mt-3 rounded-lg bg-nexus-bg/60 p-3 text-sm text-slate-200">
          {run.finalResponse}
        </div>
      )}
    </Card>
  );
}
