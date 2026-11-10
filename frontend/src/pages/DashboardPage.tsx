import { Link } from "react-router-dom";
import EscalationQueue from "../components/dashboard/EscalationQueue";
import KpiGrid from "../components/dashboard/KpiGrid";
import LiveCasesList from "../components/dashboard/LiveCasesList";
import ResolutionChart from "../components/dashboard/ResolutionChart";
import { Button } from "../components/ui/button";
import { useAuth } from "../auth/AuthProvider";
import SystemMetrics from "../components/dashboard/SystemMetrics";

export default function DashboardPage() {
  const { user } = useAuth();
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