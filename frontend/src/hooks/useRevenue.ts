import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getRevenueSummary,
  listOpportunities,
  scanOpportunities,
  triggerFollowup,
} from "../services/revenueService";

export function useRevenueSummary(merchantId?: string) {
  return useQuery({
    queryKey: ["revenue-summary", merchantId],
    queryFn: () => getRevenueSummary(merchantId),
  });
}

export function useOpportunities(merchantId?: string) {
  return useQuery({
    queryKey: ["revenue-opps", merchantId],
    queryFn: () => listOpportunities(merchantId),
  });
}

export function useTriggerFollowup() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => triggerFollowup(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["revenue-opps"] }),
  });
}

export function useScanOpportunities() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (merchantId: string) => scanOpportunities(merchantId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["revenue-opps"] });
      qc.invalidateQueries({ queryKey: ["revenue-summary"] });
    },
  });
}
