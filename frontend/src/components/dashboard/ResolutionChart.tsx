import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../services/api";
import { Card, CardTitle } from "../ui/card";

const demoData = [
  { name: "Rule-based", resolved: 42, time: 380 },
  { name: "LLM Chatbot", resolved: 58, time: 210 },
  { name: "NEXUS AI", resolved: 91, time: 62 },
];

interface Evaluation {
  intent_accuracy: number;
  resolution_rate: number;
  total: number;
  comparison: { name: string; resolved: number; time: number }[];
}

export default function ResolutionChart() {
  const { data } = useQuery({
    queryKey: ["evaluation"],
    queryFn: async () => {
      const response = await api.get<Evaluation>("/agent/evaluation");
      return response.data;
    },
    retry: false,
  });
  const chartData = data?.comparison ?? demoData;

  return (
    <Card>
      <CardTitle>Resolution Performance Comparison</CardTitle>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E2D4A" />
            <XAxis dataKey="name" stroke="#94A3B8" fontSize={12} />
            <YAxis stroke="#94A3B8" fontSize={12} />
            <Tooltip
              contentStyle={{
                background: "#111C33",
                border: "1px solid #1E2D4A",
              }}
            />
            <Bar dataKey="resolved" fill="#00B9F1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-2 text-[11px] text-nexus-muted">
        {data
          ? `Live: ${(data.intent_accuracy * 100).toFixed(1)}% intent accuracy; ${(data.resolution_rate * 100).toFixed(1)}% verified outcomes over ${data.total} cases.`
          : "Run backend evaluation to load live results. Showing demo data."}
      </div>
    </Card>
  );
}
