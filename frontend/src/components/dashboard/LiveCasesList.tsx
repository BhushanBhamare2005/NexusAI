import { Link } from "react-router-dom";
import { Card, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { useAgentRuns } from "../../hooks/useAgent";
import { shortId, formatDate } from "../../lib/formatters";

const toneFor: Record<string, "success" | "warn" | "danger" | "accent"> = {
  resolved: "success",
  running: "accent",
  awaiting_approval: "warn",
  escalated: "danger",
  failed: "danger",
};

export default function LiveCasesList() {
  const { data: runs = [] } = useAgentRuns(10);

  return (
    <Card>
      <CardTitle>Live Cases</CardTitle>
      <div className="space-y-2">
        {runs.length === 0 && (
          <div className="text-xs text-nexus-muted">No cases yet.</div>
        )}
        {runs.map((r) => (
          <Link
            key={r.runId}
            to={`/agent?run=${r.runId}`}
            className="block rounded-lg border border-nexus-border/60 p-3 hover:border-nexus-accent/50"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-white">
                Case {shortId(r.caseId)}
              </span>
              <Badge tone={toneFor[r.status] || "neutral"}>
                {r.status.replace("_", " ")}
              </Badge>
            </div>
            <div className="mt-1 text-[11px] text-nexus-muted">
              {r.intent || "Processing…"} · {formatDate(r.createdAt)}
            </div>
          </Link>
        ))}
      </div>
    </Card>
  );
}
