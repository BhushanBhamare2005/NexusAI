export interface AgentMessage {
  id: string;
  role: "user" | "agent" | "system";
  content: string;
  timestamp: string;
}

export interface AgentStep {
  step: number;
  name: string;
  status: "pending" | "running" | "done" | "failed" | "skipped";
  detail?: string;
  evidence?: Record<string, unknown>;
  startedAt?: string;
  endedAt?: string;
}

export interface ToolCall {
  id: string;
  name: string;
  args: Record<string, unknown>;
  result?: Record<string, unknown>;
  status: "pending" | "success" | "error";
  error?: string;
}

export interface AgentRun {
  runId: string;
  caseId: string;
  status: "running" | "resolved" | "awaiting_approval" | "escalated" | "failed";
  intent?: string;
  rootCause?: string;
  selectedAction?: string;
  riskLevel?: "safe" | "approval_needed" | "blocked";
  steps: AgentStep[];
  toolCalls: ToolCall[];
  finalResponse?: string;
  knowledgeEvidence?: string[];
  verified?: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AgentRunRequest {
  message: string;
  customerId?: string;
  merchantId?: string;
  transactionRef?: string;
}
