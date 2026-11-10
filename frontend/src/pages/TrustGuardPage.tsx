import ApprovalQueue from "../components/trustguard/ApprovalQueue";
import DuplicateRefundGuard from "../components/trustguard/DuplicateRefundGuard";
import PermissionMatrix from "../components/trustguard/PermissionMatrix";
import AccountManagement from "../components/trustguard/AccountManagement";
import { useAuth } from "../auth/AuthProvider";
import CustomerConsentManager from "../components/trustguard/CustomerConsentManager";

export default function TrustGuardPage() {
  const { user } = useAuth();
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-white">TrustGuard</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Review risk gates and the prototype approval queue.
        </p>
      </div>
      <ApprovalQueue />
      <div className="grid gap-4 xl:grid-cols-2">
        <DuplicateRefundGuard />
        <PermissionMatrix />
      </div>
      {user?.role === "manager" && (
        <>
          <AccountManagement />
          <CustomerConsentManager />
        </>
      )}
    </div>
  );
}