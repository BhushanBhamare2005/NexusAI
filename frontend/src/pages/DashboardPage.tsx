import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import EscalationQueue from "../components/dashboard/EscalationQueue";
import KpiGrid from "../components/dashboard/KpiGrid";
import LiveCasesList from "../components/dashboard/LiveCasesList";
import ResolutionChart from "../components/dashboard/ResolutionChart";
import { Button } from "../components/ui/button";
import { useAuth } from "../auth/AuthProvider";
import SystemMetrics from "../components/dashboard/SystemMetrics";
import { api } from "../services/api";

interface AuthorizedDashboard {
  role: "manager" | "senior_agent" | "agent";
  path: string;
}

const dashboardLabels: Record<AuthorizedDashboard["role"], string> = {
  manager: "Manager Dashboard",
  senior_agent: "Senior Agent Dashboard",
  agent: "Agent Dashboard",
};

export default function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [accessError, setAccessError] = useState("");
  const dashboards = useQuery({
    queryKey: ["authorized-dashboards", user?.role],
    queryFn: async () =>
      (await api.get<AuthorizedDashboard[]>("/auth/dashboards")).data,
    enabled: Boolean(user),
  });

  const openDashboard = async (role: AuthorizedDashboard["role"]) => {
    setAccessError("");
    try {
      const { data } = await api.get<AuthorizedDashboard>(
        `/auth/dashboards/${role}`,
      );
      navigate(data.path);
    } catch (reason) {
      setAccessError(
        reason instanceof Error
          ? reason.message
          : "Access denied. Your assigned role does not allow this dashboard.",
      );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-white">Command Center</h1>
          <p className="mt-1 text-sm text-nexus-muted">
            Payment operations and verified case outcomes.
          </p>
        </div>
        <Link to="/agent">
          <Button>Start an investigation</Button>
        </Link>
      </div>
      <section aria-labelledby="role-dashboards-heading" className="space-y-3">
        <div>
          <h2
            id="role-dashboards-heading"
            className="text-lg font-semibold text-white"
          >
            Your authorized dashboards
          </h2>
          <p className="text-sm text-nexus-muted">
            Dashboard access is verified by the server for your account.
          </p>
        </div>
        {dashboards.isLoading && (
          <p className="text-sm text-nexus-muted">Checking dashboard access…</p>
        )}
        {dashboards.isError && (
          <p role="alert" className="text-sm text-nexus-danger">
            Could not verify dashboard access: {dashboards.error.message}
          </p>
        )}
        {accessError && (
          <p role="alert" className="text-sm text-nexus-danger">
            Access denied: {accessError}
          </p>
        )}
        <div className="grid gap-3 md:grid-cols-3">
          {dashboards.data?.map((dashboard) => (
            <button
              key={dashboard.role}
              type="button"
              onClick={() => void openDashboard(dashboard.role)}
              className="rounded-xl border border-nexus-border bg-nexus-panel p-4 text-left transition hover:border-nexus-accent focus:outline-none focus:ring-2 focus:ring-nexus-accent"
            >
              <span className="block font-medium text-white">
                {dashboardLabels[dashboard.role]}
              </span>
              <span className="mt-1 block text-xs text-nexus-muted">
                Open your assigned workspace
              </span>
            </button>
          ))}
        </div>
      </section>
      <KpiGrid />
      <div className="grid gap-4 xl:grid-cols-2">
        <LiveCasesList />
        {user?.role !== "agent" && <EscalationQueue />}
      </div>
      <ResolutionChart />
      {user?.role === "manager" && <SystemMetrics />}
    </div>
  );
}