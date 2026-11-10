import type { RecoveryOpportunity } from "../../types/revenue";
import { Card, CardTitle } from "../ui/card";

export default function ConversionTracker({
  opportunities,
}: {
  opportunities: RecoveryOpportunity[];
}) {
  const contacted = opportunities.filter(
    (item) =>
      item.conversionStatus === "contacted" ||
      item.conversionStatus === "converted",
  ).length;
  const converted = opportunities.filter(
    (item) => item.conversionStatus === "converted",
  ).length;

  return (
    <Card>
      <CardTitle>Follow-up conversion</CardTitle>
      <div className="text-2xl font-semibold text-white">
        {converted} <span className="text-sm text-nexus-muted">converted</span>
      </div>
      <p className="mt-1 text-xs text-nexus-muted">
        {contacted} of {opportunities.length} opportunities contacted
      </p>
    </Card>
  );
}