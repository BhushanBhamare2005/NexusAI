import type { AuditEvent } from "../../types/audit";
import { formatDate } from "../../lib/formatters";
import { Card, CardTitle } from "../ui/card";
import { Table, THead, TR, TH, TD } from "../ui/table";

export default function EvidenceLedger({ events }: { events: AuditEvent[] }) {
  return (
    <Card>
      <CardTitle>Evidence ledger</CardTitle>
      <Table>
        <THead>
          <TR>
            <TH>Event</TH>
            <TH>Case</TH>
            <TH>Actor</TH>
            <TH>Timestamp</TH>
            <TH>Hash</TH>
          </TR>
        </THead>
        <tbody>
          {events.map((event) => (
            <TR key={event.id}>
              <TD>{event.eventType}</TD>
              <TD className="font-mono">{event.caseId}</TD>
              <TD>{event.actor}</TD>
              <TD>{formatDate(event.timestamp)}</TD>
              <TD className="font-mono text-xs">{event.hash.slice(0, 16)}…</TD>
            </TR>
          ))}
          {events.length === 0 && (
            <TR>
              <TD colSpan={5}>No audit events have been recorded.</TD>
            </TR>
          )}
        </tbody>
      </Table>
    </Card>
  );
}