import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { useAuth } from "../auth/AuthProvider";
import { Card, CardTitle } from "../components/ui/card";
import { api } from "../services/api";

interface DemoMetric {
  label: string;
  value: number;
  unit?: string;
}

interface DemoDashboard {
  label: string;
  notice: string;
  scope: "team" | "assigned_team" | "personal";
  profile: { name: string; title: string } | null;
  metrics: DemoMetric[];
  team_members: {
    name: string;
    role: string;
    status: string;
    completion_rate: number;
  }[];
  tasks: {
    id: string;
    title: string;
    assignee: string;
    status: string;
    progress: number;
    due: string;
  }[];
  task_analytics: { status: string; count: number }[];
  productivity: { period: string; completed: number; target: number }[];
  activities: { id: string; text: string; when: string }[];
  reports: { title: string; summary: string }[];
}

export default function DemoDashboardPage() {
  const { user } = useAuth();
  const isManager = user?.role === "demo_manager";
  const isSeniorAgent = user?.role === "demo_senior_agent";
  const dashboard = useQuery({
    queryKey: ["demo-dashboard", user?.role],
    queryFn: async () =>
      (await api.get<DemoDashboard>("/demo/dashboard")).data,
  });

  const dashboardTitle = isManager
    ? "Manager operations overview"
    : isSeniorAgent
      ? "Senior Agent team desk"
      : "Agent service workspace";
  const dashboardDescription = isManager
    ? "Monitor fictional team capacity, task progress, and performance summaries."
    : isSeniorAgent
      ? "Coordinate your assigned fictional agents and review team workload."
      : "Track your fictional assignments, progress, and personal performance.";

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
      {dashboard.isLoading && (
        <p className="text-sm text-nexus-muted">Loading demo data…</p>
      )}
      {dashboard.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load demo data: {dashboard.error.message}
        </p>
      )}
      {dashboard.data && (
        <>
          <div
            role="note"
            className="rounded-lg border border-nexus-warn/30 bg-nexus-warn/10 p-4 text-sm text-nexus-warn"
          >
            {dashboard.data.notice}
          </div>
          {dashboard.data.profile && (
            <Card>
              <p className="text-xs uppercase tracking-wide text-nexus-muted">
                {dashboard.data.profile.title} demo profile
              </p>
              <p className="mt-1 text-xl font-semibold text-white">
                {dashboard.data.profile.name}
              </p>
              <p className="mt-1 text-xs text-nexus-muted">
                {dashboard.data.label}
              </p>
            </Card>
          )}
          {isManager ? (
            <ManagerDemoView dashboard={dashboard.data} />
          ) : isSeniorAgent ? (
            <SeniorAgentDemoView dashboard={dashboard.data} />
          ) : (
            <AgentDemoView dashboard={dashboard.data} />
          )}
        </>
      )}
    </div>
  );
}

function ManagerDemoView({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <>
      <MetricCards metrics={dashboard.metrics} />
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <ProductivityChart dashboard={dashboard} title="Team productivity" />
        <TaskAnalytics dashboard={dashboard} />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <TeamMembers dashboard={dashboard} />
        <TaskList dashboard={dashboard} title="Team task assignments" />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <ActivityList dashboard={dashboard} title="Recent team activity" />
        <Reports dashboard={dashboard} />
      </div>
    </>
  );
}

function SeniorAgentDemoView({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <>
      <MetricCards metrics={dashboard.metrics} />
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <ProductivityChart dashboard={dashboard} title="Assigned-team productivity" />
        <TaskAnalytics dashboard={dashboard} />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <TeamMembers dashboard={dashboard} />
        <TaskList dashboard={dashboard} title="Assigned team tasks" />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <ActivityList dashboard={dashboard} title="Recent team activity" />
        <Reports dashboard={dashboard} />
      </div>
    </>
  );
}

function AgentDemoView({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <>
      <MetricCards metrics={dashboard.metrics} />
      <div className="grid gap-4 xl:grid-cols-[1.4fr_0.6fr]">
        <ProductivityChart dashboard={dashboard} title="Personal productivity" />
        <TaskAnalytics dashboard={dashboard} />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <TaskList dashboard={dashboard} title="My assigned demo tasks" />
        <ActivityList dashboard={dashboard} title="Recent personal activity" />
      </div>
      <Reports dashboard={dashboard} />
    </>
  );
}

function MetricCards({ metrics }: { metrics: DemoMetric[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.label}>
          <p className="text-sm text-nexus-muted">{metric.label}</p>
          <p className="mt-2 text-3xl font-semibold text-white">
            {metric.value}
            {metric.unit ?? ""}
          </p>
        </Card>
      ))}
    </div>
  );
}

function ProductivityChart({
  dashboard,
  title,
}: {
  dashboard: DemoDashboard;
  title: string;
}) {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={dashboard.productivity}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E2D4A" />
            <XAxis dataKey="period" stroke="#94A3B8" fontSize={12} />
            <YAxis stroke="#94A3B8" fontSize={12} allowDecimals={false} />
            <Tooltip
              contentStyle={{
                background: "#111C33",
                border: "1px solid #1E2D4A",
              }}
            />
            <Legend />
            <Bar
              dataKey="completed"
              name="Completed"
              fill="#00B9F1"
              radius={[4, 4, 0, 0]}
            />
            <Bar
              dataKey="target"
              name="Target"
              fill="#64748B"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-2 text-xs text-nexus-muted">
        Fictional completed-task counts compared with the daily demo target.
      </p>
    </Card>
  );
}

function TaskAnalytics({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <Card>
      <CardTitle>Task completion analytics</CardTitle>
      <div className="space-y-4">
        {dashboard.task_analytics.map((item) => {
          const total = dashboard.tasks.length || 1;
          const percentage = Math.round((item.count / total) * 100);
          return (
            <div key={item.status}>
              <div className="flex justify-between gap-2 text-sm">
                <span className="text-white">{item.status}</span>
                <span className="text-nexus-muted">
                  {item.count} ({percentage}%)
                </span>
              </div>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-nexus-border">
                <div
                  className="h-full rounded-full bg-nexus-accent"
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
      <p className="mt-4 text-xs text-nexus-muted">
        Based on {dashboard.tasks.length} synthetic tasks in this view.
      </p>
    </Card>
  );
}

function TeamMembers({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <Card>
      <CardTitle>
        {dashboard.scope === "team" ? "Team performance overview" : "Assigned agents"}
      </CardTitle>
      <div className="space-y-3">
        {dashboard.team_members.map((member) => (
          <div
            key={`${member.role}-${member.name}`}
            className="rounded-lg border border-nexus-border p-3"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <p className="text-sm font-medium text-white">{member.name}</p>
                <p className="text-xs text-nexus-muted">{member.role}</p>
              </div>
              <span className="text-xs text-nexus-accent">{member.status}</span>
            </div>
            <div className="mt-3 flex justify-between text-xs text-nexus-muted">
              <span>Completion</span>
              <span>{member.completion_rate}%</span>
            </div>
            <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-nexus-border">
              <div
                className="h-full rounded-full bg-nexus-accent"
                style={{ width: `${member.completion_rate}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

function TaskList({
  dashboard,
  title,
}: {
  dashboard: DemoDashboard;
  title: string;
}) {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      <div className="space-y-3">
        {dashboard.tasks.map((task) => (
          <div
            key={task.id}
            className="rounded-lg border border-nexus-border p-3"
          >
            <div className="flex flex-wrap justify-between gap-2">
              <div>
                <p className="text-xs text-nexus-accent">{task.id}</p>
                <p className="mt-1 text-sm text-white">{task.title}</p>
                {dashboard.scope !== "personal" && (
                  <p className="mt-1 text-xs text-nexus-muted">
                    Assigned to {task.assignee}
                  </p>
                )}
              </div>
              <span className="self-start text-xs text-nexus-muted">
                {task.status}
              </span>
            </div>
            <div className="mt-3 flex justify-between text-xs text-nexus-muted">
              <span>{task.progress}% complete</span>
              <span>Due {task.due.toLowerCase()}</span>
            </div>
            <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-nexus-border">
              <div
                className="h-full rounded-full bg-nexus-accent"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

function ActivityList({
  dashboard,
  title,
}: {
  dashboard: DemoDashboard;
  title: string;
}) {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      <div className="space-y-3">
        {dashboard.activities.map((activity) => (
          <div key={activity.id} className="border-l-2 border-nexus-accent pl-3">
            <p className="text-sm text-white">{activity.text}</p>
            <p className="mt-1 text-xs text-nexus-muted">{activity.when}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}

function Reports({ dashboard }: { dashboard: DemoDashboard }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {dashboard.reports.map((report) => (
        <Card key={report.title}>
          <CardTitle>{report.title}</CardTitle>
          <p className="text-sm leading-6 text-nexus-muted">{report.summary}</p>
        </Card>
      ))}
    </div>
  );
}
