import type { RecoveryOpportunity } from "../../types/revenue";
import { useTriggerFollowup } from "../../hooks/useRevenue";
import { formatINR, formatDate } from "../../lib/formatters";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card } from "../ui/card";

export default function RecoveryOpportunityCard({
  opportunity,
}: {
  opportunity: RecoveryOpportunity;
}) {
  const followup = useTriggerFollowup();

  return (
    <Card>
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-sm text-white">{opportunity.txnRef}</span>
        <Badge
          tone={
            opportunity.conversionStatus === "converted" ? "success" : "warn"
          }
        >
          {opportunity.conversionStatus.replace("_", " ")}
        </Badge>
      </div>
      <div className="mt-2 text-lg font-semibold text-nexus-accent">
        {formatINR(opportunity.amount)}
      </div>
      <p className="mt-1 text-xs text-nexus-muted">
        {opportunity.rootCause} · {formatDate(opportunity.createdAt)}
      </p>
      <p className="mt-3 text-sm text-slate-300">
        {opportunity.recommendedAction}
      </p>
      {opportunity.followupMessage && (
        <p className="mt-2 rounded-lg bg-nexus-bg p-2 text-xs text-slate-300">
          {opportunity.followupMessage}
        </p>
      )}
      {opportunity.notificationMode === "simulated" && (
        <p className="mt-2 text-xs text-nexus-warn">
          Simulation only — no SMS was sent.
        </p>
      )}
      {opportunity.notificationMode === "twilio" &&
        opportunity.notificationStatus !== "delivered" && (
          <p className="mt-2 text-xs text-nexus-warn">
            Twilio accepted the message; delivery is not yet confirmed.
          </p>
        )}
      {opportunity.notificationError && (
        <p role="alert" className="mt-2 text-xs text-nexus-danger">
          Message not sent: {opportunity.notificationError}
        </p>
      )}
      {followup.isError && (
        <p role="alert" className="mt-2 text-xs text-nexus-danger">
          {followup.error.message}
        </p>
      )}
      {opportunity.conversionStatus === "not_contacted" && (
        <Button
          className="mt-3"
          disabled={followup.isPending}
          onClick={() => followup.mutate(opportunity.id)}
        >
          Send simulated follow-up
        </Button>
      )}
    </Card>
  );
}