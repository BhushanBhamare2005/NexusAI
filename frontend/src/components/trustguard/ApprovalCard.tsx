import type { Approval } from "../../types/trustguard";
import { useDecideApproval } from "../../hooks/useApprovals";
import { formatDate } from "../../lib/formatters";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card } from "../ui/card";

export default function ApprovalCard({ approval }: { approval: Approval }) {
  const decision = useDecideApproval();

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="font-medium text-white">{approval.action}</div>
          <div className="mt-1 text-xs text-nexus-muted">
            Case {approval.caseId} · {formatDate(approval.createdAt)}
          </div>
        </div>
        <Badge tone={approval.status === "pending" ? "warn" : "neutral"}>
          {approval.status}
        </Badge>
      </div>
      <p className="my-3 text-sm text-slate-300">{approval.reason}</p>
      {decision.isError && (
        <p role="alert" className="mb-2 text-xs text-nexus-danger">
          {decision.error.message}
        </p>
      )}
      {approval.status === "pending" && (
        <div className="flex gap-2">
          <Button
            disabled={decision.isPending}
            onClick={() =>
              decision.mutate({ id: approval.id, decision: "approved" })
            }
          >
            Approve
          </Button>
          <Button
            variant="danger"
            disabled={decision.isPending}
            onClick={() =>
              decision.mutate({ id: approval.id, decision: "rejected" })
            }
          >
            Reject
          </Button>
        </div>
      )}
    </Card>
  );
}