export const RISK_LEVELS = ["safe", "approval_needed", "blocked"] as const;
export type RiskLevel = (typeof RISK_LEVELS)[number];

export const STEP_LABELS = [
  "Understand",
  "Investigate",
  "Diagnose",
  "Decide",
  "Execute",
  "Verify",
  "Deliver",
  "Escalate",
] as const;

export const STATUS_COLORS: Record<string, string> = {
  success: "text-nexus-success",
  pending: "text-nexus-warn",
  failed: "text-nexus-danger",
  refunded: "text-nexus-accent",
};
