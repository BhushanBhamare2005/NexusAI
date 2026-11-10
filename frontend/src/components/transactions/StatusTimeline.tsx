import { Card, CardTitle } from "../ui/card";
import { formatDate } from "../../lib/formatters";

interface Event {
  status: string;
  at: string;
  note?: string;
}

export default function StatusTimeline({ events }: { events: Event[] }) {
  return (
    <Card>
      <CardTitle>Status History</CardTitle>
      <div className="space-y-2">
        {events.map((e, i) => (
          <div key={i} className="flex gap-3 text-xs">
            <div className="mt-1 h-2 w-2 rounded-full bg-nexus-accent" />
            <div>
              <div className="text-white">{e.status}</div>
              <div className="text-[10px] text-nexus-muted">
                {formatDate(e.at)} {e.note && `· ${e.note}`}
              </div>
            </div>
          </div>
        ))}
        {events.length === 0 && (
          <div className="text-xs text-nexus-muted">No events.</div>
        )}
      </div>
    </Card>
  );
}
