import type { AuditEvent } from "../../types/audit";
import { formatDate } from "../../lib/formatters";
import { Card, CardTitle } from "../ui/card";

export default function CaseHistory({ events }: { events: AuditEvent[] }) {
  return (
    <Card>
      <CardTitle>Case history</CardTitle>
      <div className="space-y-3">
        {events.map((event) => (
          <div key={event.id} className="border-l border-nexus-accent/50 pl-3">
            <div className="text-sm text-white">{event.eventType}</div>
            <div className="text-xs text-nexus-muted">
              {event.caseId} · {formatDate(event.timestamp)}
            </div>
          </div>
        ))}
        {events.length === 0 && (
          <p className="text-sm text-nexus-muted">No case history yet.</p>
        )}
      </div>
    </Card>
  );
}