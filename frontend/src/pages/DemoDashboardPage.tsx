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
  const isManager = user?.role === "demo_manager";
  const isSeniorAgent = user?.role === "demo_senior_agent";
  const overview = useQuery({
    queryKey: ["demo-overview"],
    queryFn: async () => (await api.get<DemoOverview>("/demo/overview")).data,
  });

  const dashboardTitle = isManager
    ? "Manager operations overview"
    : isSeniorAgent
      ? "Senior Agent escalation desk"
      : "Agent service workspace";
  const dashboardDescription = isManager
    ? "Review synthetic operations, risk cases, and team-access status."
    : isSeniorAgent
      ? "Triage synthetic escalations and review recovery workload."
      : "Work through synthetic customer cases and monitor resolution progress.";

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-medium uppercase tracking-wide text-nexus-accent">
          Restricted, read-only demo sandbox
        </p>
        <h1 className="mt-1 text-2xl font-semibold text-white">
          {dashboardTitle}
        </h1>
        <p className="mt-1 text-sm text-nexus-muted">{dashboardDescription}</p>
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
          {isManager ? (
            <ManagerDemoView overview={overview.data} />
          ) : isSeniorAgent ? (
            <SeniorAgentDemoView overview={overview.data} />
          ) : (
            <AgentDemoView overview={overview.data} />
          )}
        </>
      )}
    </div>
  );
}

function ManagerDemoView({ overview }: { overview: DemoOverview }) {
  return (
    <>
      <MetricCards overview={overview} />
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <CaseList title="Risk and approval review" overview={overview} />
        <Card>
          <CardTitle>Team access</CardTitle>
          <p className="mt-2 text-sm text-nexus-muted">
            Role assignments and account changes are disabled for shared demo
            accounts. Production user administration remains protected.
          </p>
          <div className="mt-4 rounded-lg border border-nexus-border p-3 text-sm">
            <div className="text-white">Access control status</div>
            <div className="mt-1 text-xs text-nexus-accent">
              Read-only · Synthetic data only
            </div>
          </div>
        </Card>
      </div>
    </>
  );
}

function SeniorAgentDemoView({ overview }: { overview: DemoOverview }) {
  return (
    <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
      <CaseList title="Escalation review queue" overview={overview} />
      <div className="space-y-4">
        <MetricCards overview={overview} layout="stacked" />
        <Card>
          <CardTitle>Recovery workflow</CardTitle>
          <p className="mt-2 text-sm text-nexus-muted">
            Review sample cases here. Recovery actions are not sent to
            customers or payment systems from this demo.
          </p>
        </Card>
      </div>
    </div>
  );
}

function AgentDemoView({ overview }: { overview: DemoOverview }) {
  return (
    <>
      <MetricCards overview={overview} />
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <CaseList title="Assigned customer cases" overview={overview} />
        <Card>
          <CardTitle>Workspace guide</CardTitle>
          <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-nexus-muted">
            <li>Review the case summary and current status.</li>
            <li>Escalate risk decisions to a senior agent in your real workflow.</li>
            <li>Use production tools only with an authorized operational account.</li>
          </ol>
        </Card>
      </div>
    </>
  );
}

function MetricCards({
  overview,
  layout = "row",
}: {
  overview: DemoOverview;
  layout?: "row" | "stacked";
}) {
  return (
    <div
      className={`grid gap-4 ${
        layout === "stacked" ? "grid-cols-1" : "md:grid-cols-3"
      }`}
    >
      {overview.metrics.map((metric) => (
        <Card key={metric.label}>
          <p className="text-sm text-nexus-muted">{metric.label}</p>
          <p className="mt-2 text-3xl font-semibold text-white">
            {metric.value}
          </p>
        </Card>
      ))}
    </div>
  );
}

function CaseList({
  title,
  overview,
}: {
  title: string;
  overview: DemoOverview;
}) {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      <p className="mt-1 text-xs text-nexus-muted">{overview.label}</p>
      <div className="mt-3 space-y-2">
        {overview.recent_cases.map((item) => (
          <div
            key={item.id}
            className="flex flex-wrap justify-between gap-2 rounded-lg border border-nexus-border p-3 text-sm"
          >
            <div>
              <div className="text-white">{item.id}</div>
              <div className="mt-1 text-xs text-nexus-muted">{item.issue}</div>
            </div>
            <span className="self-center text-xs text-nexus-accent">
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
}
