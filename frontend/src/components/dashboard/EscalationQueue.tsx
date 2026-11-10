import { Link } from "react-router-dom";
import { Card, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { useApprovals } from "../../hooks/useApprovals";

export default function EscalationQueue() {
  const { data: approvals = [] } = useApprovals();

  return (
    <Card>
      <CardTitle>Escalation Queue</CardTitle>
      {approvals.length === 0 ? (
        <div className="text-xs text-nexus-muted">No pending approvals.</div>
      ) : (
        <div className="space-y-2">
          {approvals.map((a) => (
            <Link
              key={a.id}
              to="/trustguard"
              className="block rounded-lg border border-nexus-warn/40 bg-nexus-warn/5 p-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm text-white">{a.action}</span>
                <Badge tone="warn">needs approval</Badge>
              </div>
              <div className="mt-1 text-[11px] text-nexus-muted">
                {a.reason}
              </div>
            </Link>
          ))}
        </div>
      )}
    </Card>
  );
}
