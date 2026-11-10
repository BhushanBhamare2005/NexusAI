import { useQuery } from "@tanstack/react-query";
import { api } from "../../services/api";
import { Card, CardTitle } from "../ui/card";

interface Metrics {
  http: {
    total: number;
    errors: number;
    duration_ms_total: number;
    status_codes: Record<string, number>;
  };
  llm: {
    requests: number;
    successes: number;
    fallbacks: number;
    errors: number;
  };
}

export default function SystemMetrics() {
  const query = useQuery({
    queryKey: ["system-metrics"],
    queryFn: async () => (await api.get<Metrics>("/health/metrics")).data,
    refetchInterval: 10000,
  });

  if (query.isError) {
    return (
      <Card>
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load system metrics: {query.error.message}
        </p>
      </Card>
    );
  }
  if (!query.data) return <Card>Loading system metrics…</Card>;

  const { http, llm } = query.data;
  const averageLatency =
    http.total > 0 ? (http.duration_ms_total / http.total).toFixed(1) : "0.0";

  return (
    <Card>
      <CardTitle>Operational metrics</CardTitle>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Metric label="HTTP requests" value={http.total} />
        <Metric label="Server errors" value={http.errors} />
        <Metric label="Average latency" value={`${averageLatency} ms`} />
        <Metric
          label="LLM success / fallback"
          value={`${llm.successes} / ${llm.fallbacks}`}
        />
      </div>
    </Card>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div>
      <div className="text-xs text-nexus-muted">{label}</div>
      <div className="mt-1 text-lg font-semibold text-white">{value}</div>
    </div>
  );
}
