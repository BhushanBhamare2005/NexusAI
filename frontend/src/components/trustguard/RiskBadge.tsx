import { Badge } from "../ui/badge";
import type { RiskLevel } from "../../types/trustguard";

const toneByLevel: Record<RiskLevel, "success" | "warn" | "danger"> = {
  safe: "success",
  approval_needed: "warn",
  blocked: "danger",
};

export default function RiskBadge({ level }: { level: RiskLevel }) {
  return <Badge tone={toneByLevel[level]}>{level.replace("_", " ")}</Badge>;
}