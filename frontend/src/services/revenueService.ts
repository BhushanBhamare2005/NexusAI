import { api } from "./api";
import type { RecoveryOpportunity, RevenueSummary } from "../types/revenue";

export async function getRevenueSummary(
  merchantId?: string
): Promise<RevenueSummary> {
  const { data } = await api.get<RevenueSummary>("/revenue/summary", {
    params: merchantId ? { merchantId } : {},
  });
  return data;
}

export async function listOpportunities(
  merchantId?: string
): Promise<RecoveryOpportunity[]> {
  const { data } = await api.get<RecoveryOpportunity[]>(
    "/revenue/opportunities",
    { params: merchantId ? { merchantId } : {} }
  );
  return data;
}

export async function triggerFollowup(id: string): Promise<RecoveryOpportunity> {
  const { data } = await api.post<RecoveryOpportunity>(
    `/revenue/opportunities/${id}/followup`
  );
  return data;
}

export async function scanOpportunities(
  merchantId: string
): Promise<{ created: number }> {
  const { data } = await api.post<{ created: number }>(
    "/revenue/opportunities/scan",
    null,
    { params: { merchantId } }
  );
  return data;
}
