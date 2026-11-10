import type { AuditEvent, LedgerVerification } from "../../types/audit";
import { Card, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";

export default function HashChainViewer({
  events,
  verification,
}: {
  events: AuditEvent[];
  verification?: LedgerVerification;
}) {
  return (
    <Card>
      <div className="flex items-center justify-between gap-3">
        <CardTitle>Hash-chain verification</CardTitle>
        {verification && (
          <Badge tone={verification.valid ? "success" : "danger"}>
            {verification.valid ? "Valid" : "Invalid"}
          </Badge>
        )}
      </div>
      <p className="text-sm text-slate-300">
        {verification
          ? `${verification.checkedEvents} events checked`
          : "Verification has not run yet."}
      </p>
      {verification?.brokenAt && (
        <p className="mt-2 text-xs text-nexus-danger">
          Chain mismatch at event {verification.brokenAt}.
        </p>
      )}
      {events.length > 0 && (
        <div className="mt-3 space-y-2">
          {events.slice(0, 5).map((event) => (
            <div key={event.id} className="rounded-lg bg-nexus-bg p-2">
              <div className="text-xs text-white">{event.eventType}</div>
              <div className="break-all font-mono text-[10px] text-nexus-muted">
                {event.prevHash.slice(0, 16)}… → {event.hash.slice(0, 16)}…
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}