import ConversionTracker from "../components/revenue/ConversionTracker";
import FailedPaymentsTable from "../components/revenue/FailedPaymentsTable";
import RecoveryFunnel from "../components/revenue/RecoveryFunnel";
import RecoveryOpportunityCard from "../components/revenue/RecoveryOpportunityCard";
import { Card } from "../components/ui/card";
import {
  useOpportunities,
  useRevenueSummary,
  useScanOpportunities,
} from "../hooks/useRevenue";
import { formatINR } from "../lib/formatters";
import { Button } from "../components/ui/button";
import { useState } from "react";
import { useAuth } from "../auth/AuthProvider";

export default function RevenuePage() {
  const summary = useRevenueSummary();
  const opportunities = useOpportunities();
  const [merchantId, setMerchantId] = useState("m_001");
  const scan = useScanOpportunities();
  const { user } = useAuth();

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold text-white">Revenue Rescue</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Review recoverable payment attempts and follow-up outcomes.
        </p>
      </div>
      {user?.role === "manager" && <form
        className="flex flex-wrap gap-2"
        onSubmit={(event) => {
          event.preventDefault();
          scan.mutate(merchantId.trim());
        }}
      >
        <input
          value={merchantId}
          onChange={(event) => setMerchantId(event.target.value)}
          aria-label="Merchant ID to scan"
          className="min-w-[220px] rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
        />
        <Button type="submit" disabled={!merchantId.trim() || scan.isPending}>
          Scan merchant
        </Button>
      </form>}
      {scan.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not scan opportunities: {scan.error.message}
        </p>
      )}
      {(summary.isError || opportunities.isError) && (
        <Card>
          <p role="alert" className="text-sm text-nexus-danger">
            Could not load revenue data:{" "}
            {summary.error?.message || opportunities.error?.message}
          </p>
        </Card>
      )}
      {summary.data && (
        <>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Metric label="Payment attempts" value={summary.data.totalAttempts} />
            <Metric label="Failed" value={summary.data.failed} />
            <Metric
              label="Opportunities"
              value={summary.data.opportunitiesIdentified}
            />
            <Metric
              label="Recovered"
              value={formatINR(summary.data.recoveredAmount)}
            />
          </div>
          <RecoveryFunnel summary={summary.data} />
        </>
      )}
      {opportunities.isLoading && <Card>Loading opportunities…</Card>}
      {opportunities.data && (
        <>
          <ConversionTracker opportunities={opportunities.data} />
          <div className="grid gap-3 lg:grid-cols-2">
            {opportunities.data.map((opportunity) => (
              <RecoveryOpportunityCard
                key={opportunity.id}
                opportunity={opportunity}
              />
            ))}
            {opportunities.data.length === 0 && (
              <Card>No opportunities yet. Scan a merchant from the API.</Card>
            )}
          </div>
        </>
      )}
      <FailedPaymentsTable />
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <Card>
      <div className="text-xs text-nexus-muted">{label}</div>
      <div className="mt-1 text-xl font-semibold text-white">{value}</div>
    </Card>
  );
}