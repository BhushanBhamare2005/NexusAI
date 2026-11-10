export type RiskLevel = "safe" | "approval_needed" | "blocked";

export interface RiskAssessment {
  level: RiskLevel;
  score: number;
  reasons: string[];
  duplicateCheck?: {
    isDuplicate: boolean;
    existingRefundId?: string;
  };
}

export interface Approval {
  id: string;
  caseId: string;
  runId: string;
  action: string;
  requestedBy: string;
  reason: string;
  riskLevel: RiskLevel;
  status: "pending" | "approved" | "rejected";
  createdAt: string;
  decidedAt?: string;
  decidedBy?: string;
}
