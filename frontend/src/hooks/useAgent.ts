import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  startAgentRun,
  getAgentRun,
  listAgentRuns,
} from "../services/agentService";
import type { AgentRunRequest } from "../types/agent";

export function useStartAgentRun() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (req: AgentRunRequest) => startAgentRun(req),
    onSuccess: (run) => {
      qc.invalidateQueries({ queryKey: ["agent-runs"] });
      qc.setQueryData(["agent-run", run.runId], run);
    },
  });
}

export function useAgentRun(runId?: string) {
  return useQuery({
    queryKey: ["agent-run", runId],
    queryFn: () => getAgentRun(runId!),
    enabled: !!runId,
    refetchInterval: 2000,
  });
}

export function useAgentRuns(limit = 20) {
  return useQuery({
    queryKey: ["agent-runs", limit],
    queryFn: () => listAgentRuns(limit),
    refetchInterval: 5000,
  });
}
