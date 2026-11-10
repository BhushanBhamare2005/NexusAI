import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { RevenueSummary } from "../../types/revenue";
import { Card, CardTitle } from "../ui/card";

export default function RecoveryFunnel({
  summary,
}: {
  summary: RevenueSummary;
}) {
  const data = [
    { stage: "Attempts", count: summary.totalAttempts },
    { stage: "Failed", count: summary.failed },
    { stage: "Opportunities", count: summary.opportunitiesIdentified },
    { stage: "Recovered", count: summary.recovered },
  ];

  return (
    <Card>
      <CardTitle>Payment recovery funnel</CardTitle>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid stroke="#1E2D4A" strokeDasharray="3 3" />
            <XAxis dataKey="stage" stroke="#94A3B8" fontSize={11} />
            <YAxis allowDecimals={false} stroke="#94A3B8" fontSize={11} />
            <Tooltip
              contentStyle={{
                background: "#111C33",
                border: "1px solid #1E2D4A",
              }}
            />
            <Bar dataKey="count" fill="#00B9F1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}