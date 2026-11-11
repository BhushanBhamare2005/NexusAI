import { useQuery } from "@tanstack/react-query";

import { useAuth } from "../auth/AuthProvider";
import { Card, CardTitle } from "../components/ui/card";
import { api } from "../services/api";

interface DemoOverview {
  label: string;
  notice: string;
  metrics: { label: string; value: number }[];
  recent_cases: { id: string; issue: string; status: string }[];
}

export default function DemoDashboardPage() {
  const { user } = useAuth();
  const overview = useQuery({
    queryKey: ["demo-overview"],
    queryFn: async () => (await api.get<DemoOverview>("/demo/overview")).data,
  });

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-medium uppercase tracking-wide text-nexus-accent">
          Restricted demo sandbox
        </p>
        <h1 className="mt-1 text-2xl font-semibold text-white">
          {user?.role.replaceAll("_", " ")} dashboard
        </h1>
      </div>
      {overview.isLoading && (
        <p className="text-sm text-nexus-muted">Loading demo data…</p>
      )}
      {overview.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load demo data: {overview.error.message}
        </p>
      )}
      {overview.data && (
        <>
          <div
            role="note"
            className="rounded-lg border border-nexus-warn/30 bg-nexus-warn/10 p-4 text-sm text-nexus-warn"
          >
            {overview.data.notice}
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {overview.data.metrics.map((metric) => (
              <Card key={metric.label}>
                <p className="text-sm text-nexus-muted">{metric.label}</p>
                <p className="mt-2 text-3xl font-semibold text-white">
                  {metric.value}
                </p>
              </Card>
            ))}
          </div>
          <Card>
            <CardTitle>{overview.data.label}</CardTitle>
            <div className="mt-3 space-y-2">
              {overview.data.recent_cases.map((item) => (
                <div
                  key={item.id}
                  className="flex flex-wrap justify-between gap-2 rounded-lg border border-nexus-border p-3 text-sm"
                >
                  <span className="text-white">
                    {item.id} · {item.issue}
                  </span>
                  <span className="text-nexus-muted">{item.status}</span>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
