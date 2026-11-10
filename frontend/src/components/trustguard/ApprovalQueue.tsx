import { useApprovals } from "../../hooks/useApprovals";
import { Card, CardTitle } from "../ui/card";
import ApprovalCard from "./ApprovalCard";

export default function ApprovalQueue() {
  const approvals = useApprovals();

  if (approvals.isLoading) return <Card>Loading approvals…</Card>;
  if (approvals.isError) {
    return (
      <Card>
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load approvals: {approvals.error.message}
        </p>
      </Card>
    );
  }

  return (
    <section>
      <CardTitle>Pending approvals</CardTitle>
      {approvals.data?.length ? (
        <div className="grid gap-3 lg:grid-cols-2">
          {approvals.data.map((approval) => (
            <ApprovalCard key={approval.id} approval={approval} />
          ))}
        </div>
      ) : (
        <Card>
          <p className="text-sm text-nexus-muted">No pending approvals.</p>
        </Card>
      )}
    </section>
  );
}