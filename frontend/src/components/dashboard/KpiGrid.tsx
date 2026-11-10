import KpiCard from "./KpiCard";
import { useAgentRuns } from "../../hooks/useAgent";

export default function KpiGrid() {
  const { data: runs = [] } = useAgentRuns(50);
  const resolved = runs.filter((r) => r.status === "resolved").length;
  const pending = runs.filter((r) => r.status === "awaiting_approval").length;
  const escalated = runs.filter((r) => r.status === "escalated").length;

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
      <KpiCard label="Active Cases" value={runs.length} tone="accent" />
      <KpiCard label="Resolved" value={resolved} tone="success" />
      <KpiCard label="Awaiting Approval" value={pending} tone="warn" />
      <KpiCard label="Escalated" value={escalated} tone="danger" />
    </div>
  );
}
