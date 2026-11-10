import type { AuditEvent } from "../../types/audit";
import { Button } from "../ui/button";

export default function ResolutionReport({ events }: { events: AuditEvent[] }) {
  const download = () => {
    const report = {
      generatedAt: new Date().toISOString(),
      eventCount: events.length,
      events,
    };
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(report, null, 2)], {
        type: "application/json",
      }),
    );
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "nexus-resolution-report.json";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex items-center justify-between gap-3 rounded-xl border border-nexus-border bg-nexus-panel p-4">
      <div>
        <div className="text-sm font-semibold text-white">Resolution report</div>
        <div className="text-xs text-nexus-muted">
          Download {events.length} audit events as JSON evidence.
        </div>
      </div>
      <Button onClick={download} disabled={events.length === 0}>
        Download report
      </Button>
    </div>
  );
}