import {
  BrowserRouter,
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
import type { ReactNode } from "react";

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

  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/agent" element={<AgentWorkspacePage />} />
        <Route path="/transactions" element={<TransactionsPage />} />
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
    <Navigate to="/" replace />
  );
}
