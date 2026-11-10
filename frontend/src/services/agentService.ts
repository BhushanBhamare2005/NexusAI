import { api } from "./api";
import type { AgentRun, AgentRunRequest } from "../types/agent";

export async function startAgentRun(req: AgentRunRequest): Promise<AgentRun> {
  const { data } = await api.post<AgentRun>("/agent/run", req);
  return data;
}

export async function getAgentRun(runId: string): Promise<AgentRun> {
  const { data } = await api.get<AgentRun>(`/agent/runs/${runId}`);
  return data;
}

export async function listAgentRuns(limit = 20): Promise<AgentRun[]> {
  const { data } = await api.get<AgentRun[]>("/agent/runs", {
    params: { limit },
  });
  return data;
}
