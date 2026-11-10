import { api } from "./api";
import type { AuditEvent, LedgerVerification } from "../types/audit";

export async function listEvents(caseId?: string): Promise<AuditEvent[]> {
  const { data } = await api.get<AuditEvent[]>("/audit/events", {
    params: caseId ? { caseId } : {},
  });
  return data;
}

export async function verifyLedger(): Promise<LedgerVerification> {
  const { data } = await api.get<LedgerVerification>("/audit/verify");
  return data;
}
