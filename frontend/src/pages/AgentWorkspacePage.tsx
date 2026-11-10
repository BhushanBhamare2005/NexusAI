import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import ChatWindow from "../components/agent/ChatWindow";
import ExecutionTimeline from "../components/agent/ExecutionTimeline";
import ResolutionReceipt from "../components/agent/ResolutionReceipt";
import ToolCallCard from "../components/agent/ToolCallCard";
import ReasoningPanel from "../components/agent/ReasoningPanel";
import { Card, CardTitle } from "../components/ui/card";
import { useAgentRun, useStartAgentRun } from "../hooks/useAgent";
import type { AgentMessage, AgentRun } from "../types/agent";

export default function AgentWorkspacePage() {
  const [searchParams] = useSearchParams();
  const startRun = useStartAgentRun();
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [run, setRun] = useState<AgentRun | null>(null);
  const refreshedRun = useAgentRun(run?.runId);
  const activeRun = refreshedRun.data || run;

  const send = async (text: string) => {
    setMessages((current) => [
      ...current,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: text,
        timestamp: new Date().toISOString(),
      },
    ]);
    try {
      const result = await startRun.mutateAsync({
        message: text,
        transactionRef: searchParams.get("txn") || undefined,
      });
      setRun(result);
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "agent",
          content: result.finalResponse || "The run completed without a response.",
          timestamp: result.updatedAt,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "system",
          content: error instanceof Error ? error.message : "The request failed.",
          timestamp: new Date().toISOString(),
        },
      ]);
    }
  };

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold text-white">AI Teammate</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Investigate a simulated payment issue and review each action.
        </p>
      </div>
      {startRun.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Agent run failed: {startRun.error.message}
        </p>
      )}
      <div className="grid min-h-[32rem] gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <ChatWindow
          messages={messages}
          onSend={send}
          disabled={startRun.isPending}
        />
        <div className="space-y-4 overflow-y-auto">
          {activeRun ? (
            <>
              <Card>
                <CardTitle>Execution timeline</CardTitle>
                <ExecutionTimeline steps={activeRun.steps} />
              </Card>
              <ResolutionReceipt run={activeRun} />
              {activeRun.knowledgeEvidence?.length ? (
                <ReasoningPanel title="Retrieved policy evidence">
                  <ul className="list-disc space-y-2 pl-4">
                    {activeRun.knowledgeEvidence.map((passage, index) => (
                      <li key={index}>{passage}</li>
                    ))}
                  </ul>
                </ReasoningPanel>
              ) : null}
              {activeRun.toolCalls.length > 0 && (
                <Card>
                  <CardTitle>Tool calls</CardTitle>
                  <div className="space-y-2">
                    {activeRun.toolCalls.map((call) => (
                      <ToolCallCard key={call.id} call={call} />
                    ))}
                  </div>
                </Card>
              )}
            </>
          ) : (
            <Card>
              <CardTitle>Case evidence</CardTitle>
              <p className="text-sm text-nexus-muted">
                Send a message to start a traceable investigation.
              </p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}