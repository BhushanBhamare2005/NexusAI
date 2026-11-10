import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import CaseHistory from "../components/audit/CaseHistory";
import EvidenceLedger from "../components/audit/EvidenceLedger";
import HashChainViewer from "../components/audit/HashChainViewer";
import ResolutionReport from "../components/audit/ResolutionReport";
import NotificationHistory from "../components/audit/NotificationHistory";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { listEvents, verifyLedger } from "../services/auditService";

export default function AuditPage() {
  const [caseId, setCaseId] = useState("");
  const events = useQuery({
    queryKey: ["audit-events", caseId],
    queryFn: () => listEvents(caseId || undefined),
  });
  const verification = useMutation({ mutationFn: verifyLedger });
  const items = events.data || [];

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold text-white">Evidence Center</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Review audit events and verify their hash chain.
        </p>
      </div>
      <form
        className="flex flex-wrap gap-2"
        onSubmit={(event) => {
          event.preventDefault();
          events.refetch();
        }}
      >
        <input
          value={caseId}
          onChange={(event) => setCaseId(event.target.value)}
          placeholder="Filter by case ID (optional)"
          className="min-w-[240px] flex-1 rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
        />
        <Button type="submit" variant="outline">
          Filter
        </Button>
        <Button
          type="button"
          onClick={() => verification.mutate()}
          disabled={verification.isPending}
        >
          Verify ledger
        </Button>
      </form>
      {(events.isError || verification.isError) && (
        <Card>
          <p role="alert" className="text-sm text-nexus-danger">
            {events.error?.message || verification.error?.message}
          </p>
        </Card>
      )}
      <NotificationHistory />
      {events.isLoading ? (
        <Card>Loading audit events…</Card>
      ) : (
        <>
          <HashChainViewer events={items} verification={verification.data} />
          <ResolutionReport events={items} />
          <CaseHistory events={items} />
          <EvidenceLedger events={items} />
        </>
      )}
    </div>
  );
}