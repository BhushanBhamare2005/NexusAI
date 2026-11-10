export interface RecoveryOpportunity {
  id: string;
  merchantId: string;
  transactionId: string;
  txnRef: string;
  amount: number;
  reason: "failed" | "abandoned" | "pending";
  rootCause: string;
  recoverable: boolean;
  recommendedAction: string;
  followupMessage?: string;
  conversionStatus: "not_contacted" | "contacted" | "converted" | "lost";
  createdAt: string;
  notificationMode?: "twilio" | "simulated";
  notificationStatus?: string;
  notificationError?: string;
}

export interface RevenueSummary {
  totalAttempts: number;
  successful: number;
  failed: number;
  pending: number;
  abandoned: number;
  opportunitiesIdentified: number;
  recovered: number;
  recoveredAmount: number;
}
