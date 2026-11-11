import { useState } from "react";
import ChatWindow from "../components/agent/ChatWindow";
import { Card } from "../components/ui/card";
import type { AgentMessage } from "../types/agent";

export default function DemoAgentWorkspacePage() {
  const [messages, setMessages] = useState<AgentMessage[]>([]);

  const send = (text: string) => {
    const timestamp = new Date().toISOString();
    setMessages((current) => [
      ...current,
      {
        id: `${Date.now()}-user`,
        role: "user",
        content: text,
        timestamp,
      },
      {
        id: `${Date.now()}-demo`,
        role: "agent",
        content: getDemoResponse(text),
        timestamp,
      },
    ]);
  };

  return (
    <div className="space-y-5">
      <div>
        <p className="text-xs font-medium uppercase tracking-wide text-nexus-accent">
          Restricted demo sandbox
        </p>
        <h1 className="mt-1 text-2xl font-semibold text-white">AI Teammate</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Try a simulated payment investigation. This demo does not connect to
          live transactions, AI services, or operational tools.
        </p>
      </div>
      <Card className="border-nexus-warn/30 bg-nexus-warn/5">
        <p className="text-sm text-nexus-warn">
          Demo mode: responses are scripted examples. No transaction lookup,
          refund, notification, or other real action is performed.
        </p>
      </Card>
      <div className="grid min-h-[32rem] gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <ChatWindow messages={messages} onSend={send} />
        <Card>
          <h2 className="text-sm font-semibold text-white">
            Safe demo prompts
          </h2>
          <ul className="mt-3 list-disc space-y-2 pl-4 text-sm text-nexus-muted">
            <li>How should I investigate a delayed payment?</li>
            <li>What details should I check before escalating a refund?</li>
            <li>How do I handle a duplicate notification report?</li>
          </ul>
          <p className="mt-4 border-t border-nexus-border pt-3 text-xs text-nexus-muted">
            For real AI investigations, sign in with an authorized operational
            Agent account.
          </p>
        </Card>
      </div>
    </div>
  );
}

function getDemoResponse(message: string): string {
  const normalized = message.toLowerCase();
  if (normalized.includes("refund")) {
    return "Demo guidance: confirm the transaction reference and current refund status in your authorized system, then follow your organization's approval process. This demo cannot inspect or issue a refund.";
  }
  if (
    normalized.includes("duplicate") ||
    normalized.includes("notification")
  ) {
    return "Demo guidance: compare the notification timestamps and transaction reference, then document the duplicate for review. This sandbox has no access to customer records or notification tools.";
  }
  if (
    normalized.includes("delay") ||
    normalized.includes("payment") ||
    normalized.includes("transaction")
  ) {
    return "Demo guidance: verify the transaction reference, payment status, and merchant settlement timeline in an authorized system. Escalate unresolved cases according to your process. No live lookup was performed.";
  }
  return "I can demonstrate safe investigation guidance for delayed payments, refund reviews, or duplicate notifications. This response is scripted and does not access live records or perform actions.";
}
