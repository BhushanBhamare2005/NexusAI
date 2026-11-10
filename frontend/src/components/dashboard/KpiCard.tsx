import { Card } from "../ui/card";

interface Props {
  label: string;
  value: string | number;
  hint?: string;
  tone?: "accent" | "success" | "warn" | "danger";
}

const toneMap = {
  accent: "text-nexus-accent",
  success: "text-nexus-success",
  warn: "text-nexus-warn",
  danger: "text-nexus-danger",
} as const;

export default function KpiCard({ label, value, hint, tone = "accent" }: Props) {
  return (
    <Card>
      <div className="text-xs text-nexus-muted">{label}</div>
      <div className={`mt-1 text-2xl font-semibold ${toneMap[tone]}`}>
        {value}
      </div>
      {hint && <div className="mt-1 text-[11px] text-nexus-muted">{hint}</div>}
    </Card>
  );
}
