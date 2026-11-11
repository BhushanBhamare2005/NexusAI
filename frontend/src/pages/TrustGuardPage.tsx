import ApprovalQueue from "../components/trustguard/ApprovalQueue";
import DuplicateRefundGuard from "../components/trustguard/DuplicateRefundGuard";
import PermissionMatrix from "../components/trustguard/PermissionMatrix";
import AccountManagement from "../components/trustguard/AccountManagement";
import { useAuth } from "../auth/AuthProvider";
import CustomerConsentManager from "../components/trustguard/CustomerConsentManager";
import KpiGrid from "../components/dashboard/KpiGrid";
import LiveCasesList from "../components/dashboard/LiveCasesList";
import EscalationQueue from "../components/dashboard/EscalationQueue";
import ResolutionChart from "../components/dashboard/ResolutionChart";
import SystemMetrics from "../components/dashboard/SystemMetrics";

export default function TrustGuardPage() {
  const { user } = useAuth();
  const isManager = user?.role === "manager";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-white">
          {isManager ? "Manager Dashboard" : "TrustGuard"}
        </h1>
        <p className="mt-1 text-sm text-nexus-muted">
          {isManager
            ? "Live payment operations, risk approvals, and team administration."
            : "Review risk gates and the approval queue."}
        </p>
      </div>
      {isManager && (
        <>
          <KpiGrid />
          <div className="grid gap-4 xl:grid-cols-2">
            <LiveCasesList />
            <EscalationQueue />
          </div>
          <ResolutionChart />
          <SystemMetrics />
        </>
      )}
      <ApprovalQueue />
      <div className="grid gap-4 xl:grid-cols-2">
        <DuplicateRefundGuard />
        <PermissionMatrix />
      </div>
      {isManager && (
        <>
          <AccountManagement />
          <CustomerConsentManager />
        </>
      )}
    </div>
  );
}