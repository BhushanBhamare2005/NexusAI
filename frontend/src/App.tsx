import {
  BrowserRouter,
  Link,
  Navigate,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import AppShell from "./components/layout/AppShell";
import DashboardPage from "./pages/DashboardPage";
import AgentWorkspacePage from "./pages/AgentWorkspacePage";
import TransactionsPage from "./pages/TransactionsPage";
import TrustGuardPage from "./pages/TrustGuardPage";
import RevenuePage from "./pages/RevenuePage";
import AuditPage from "./pages/AuditPage";
import { ToastHost } from "./components/ui/toast";
import { useAuth } from "./auth/AuthProvider";
import LoginPage from "./pages/LoginPage";
import DemoDashboardPage from "./pages/DemoDashboardPage";
import DemoAgentWorkspacePage from "./pages/DemoAgentWorkspacePage";
import { useQuery } from "@tanstack/react-query";
import { api } from "./services/api";
import type { ReactNode } from "react";

interface AuthorizedDashboard {
  role: string;
  path: string;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={<AuthenticatedApp />} />
      </Routes>
    </BrowserRouter>
  );
}

function AuthenticatedApp() {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <div className="p-8 text-nexus-muted">Loading account…</div>;
  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  const demoRoutes = ["/demo", "/demo/ai-teammate"];
  if (user.role.startsWith("demo_") && !demoRoutes.includes(location.pathname)) {
    return <Navigate to="/demo" replace />;
  }

  return (
    <AppShell>
      <Routes>
        <Route
          path="/demo"
          element={
            <RequireRole
              roles={["demo_manager", "demo_senior_agent", "demo_agent"]}
            >
              <DemoDashboardPage />
            </RequireRole>
          }
        />
        <Route
          path="/demo/ai-teammate"
          element={
            <RequireRole
              roles={["demo_manager", "demo_senior_agent", "demo_agent"]}
            >
              <DemoAgentWorkspacePage />
            </RequireRole>
          }
        />
        <Route path="/" element={<AuthorizedDashboardRedirect />} />
        <Route path="/command-center" element={<DashboardPage />} />
        <Route
          path="/agent"
          element={
            <RequireRole roles={["agent", "senior_agent", "manager"]}>
              <AgentWorkspacePage />
            </RequireRole>
          }
        />
        <Route
          path="/transactions"
          element={
            <RequireRole roles={["agent", "senior_agent", "manager"]}>
              <TransactionsPage />
            </RequireRole>
          }
        />
        <Route
          path="/trustguard"
          element={
            <RequireRole roles={["senior_agent", "manager"]}>
              <TrustGuardPage />
            </RequireRole>
          }
        />
        <Route
          path="/revenue"
          element={
            <RequireRole roles={["senior_agent", "manager"]}>
              <RevenuePage />
            </RequireRole>
          }
        />
        <Route
          path="/audit"
          element={
            <RequireRole roles={["senior_agent", "manager"]}>
              <AuditPage />
            </RequireRole>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastHost />
    </AppShell>
  );
}

function AuthorizedDashboardRedirect() {
  const { user } = useAuth();
  const dashboards = useQuery({
    queryKey: ["authorized-dashboards", user?.role],
    queryFn: async () =>
      (await api.get<AuthorizedDashboard[]>("/auth/dashboards")).data,
    enabled: Boolean(user),
  });

  if (dashboards.isLoading) {
    return <div className="p-8 text-nexus-muted">Opening your dashboard…</div>;
  }
  if (dashboards.isError) {
    return (
      <div role="alert" className="p-8 text-sm text-nexus-danger">
        Could not verify your dashboard: {dashboards.error.message}
      </div>
    );
  }

  const destination = dashboards.data?.[0]?.path;
  if (!destination || destination === "/") {
    return (
      <div role="alert" className="p-8 text-sm text-nexus-danger">
        No dashboard is assigned to this account. Contact an administrator.
      </div>
    );
  }

  return <Navigate to={destination} replace />;
}

function RequireRole({
  roles,
  children,
}: {
  roles: string[];
  children: ReactNode;
}) {
  const { user } = useAuth();
  return user && roles.includes(user.role) ? (
    children
  ) : (
    <AccessDenied />
  );
}

function AccessDenied() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-nexus-bg p-4">
      <div className="max-w-md rounded-xl border border-nexus-border bg-nexus-panel p-6 text-center">
        <h1 className="text-xl font-semibold text-white">Access denied</h1>
        <p className="mt-2 text-sm text-nexus-muted">
          Your assigned role does not allow access to this dashboard.
        </p>
        <Link
          to="/"
          className="mt-4 inline-block rounded-lg bg-nexus-accent px-4 py-2 text-sm font-medium text-black"
        >
          Return to Command Center
        </Link>
      </div>
    </main>
  );
}
