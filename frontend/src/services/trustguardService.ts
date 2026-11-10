import { api } from "./api";
import type { Approval } from "../types/trustguard";

export async function listPendingApprovals(): Promise<Approval[]> {
  const { data } = await api.get<Approval[]>("/trustguard/approvals");
  return data;
}

export async function decideApproval(
  id: string,
  decision: "approved" | "rejected",
  decidedBy = "reviewer"
): Promise<Approval> {
  const { data } = await api.post<Approval>(
    `/trustguard/approvals/${id}/decide`,
    { decision, decidedBy }
  );
  return data;
}
