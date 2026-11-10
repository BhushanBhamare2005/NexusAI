import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  listPendingApprovals,
  decideApproval,
} from "../services/trustguardService";

export function useApprovals() {
  return useQuery({
    queryKey: ["approvals"],
    queryFn: listPendingApprovals,
    refetchInterval: 5000,
  });
}

export function useDecideApproval() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      decision,
    }: {
      id: string;
      decision: "approved" | "rejected";
    }) => decideApproval(id, decision),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["approvals"] }),
  });
}
