export interface AuditEvent {
  id: string;
  caseId: string;
  runId: string;
  eventType: string;
  actor: string;
  payload: Record<string, unknown>;
  prevHash: string;
  hash: string;
  timestamp: string;
}

export interface LedgerVerification {
  valid: boolean;
  checkedEvents: number;
  brokenAt?: string;
}
