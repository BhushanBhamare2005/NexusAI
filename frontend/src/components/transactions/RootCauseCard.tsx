import { Card, CardTitle } from "../ui/card";

export default function RootCauseCard({
  rootCause,
  evidence,
}: {
  rootCause: string;
  evidence: Record<string, unknown>;
}) {
  return (
    <Card>
      <CardTitle>Root Cause</CardTitle>
      <div className="text-sm text-white">{rootCause}</div>
      <div className="mt-2 text-[10px] uppercase text-nexus-muted">
        Evidence
      </div>
      <pre className="mt-1 overflow-x-auto text-[10px] text-slate-400">
        {JSON.stringify(evidence, null, 2)}
      </pre>
    </Card>
  );
}
