import { useQuery } from "@tanstack/react-query";
import { api } from "../../services/api";
import { Card, CardTitle } from "../ui/card";

interface NotificationRecord {
  id: string;
  caseId?: string | null;
  customerId?: string | null;
  channel: string;
  recipient: string;
  message: string;
  mode: "simulated" | "twilio";
  accepted: boolean;
  delivered: boolean;
  providerStatus?: string | null;
  createdAt: string;
}

export default function NotificationHistory() {
  const query = useQuery({
    queryKey: ["notification-history"],
    queryFn: async () =>
      (await api.get<NotificationRecord[]>("/notifications", {
        params: { limit: 20 },
      })).data,
  });

  return (
    <Card>
      <CardTitle>Notification delivery history</CardTitle>
      {query.isLoading && <p className="text-sm text-nexus-muted">Loading notifications…</p>}
      {query.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load notification history: {query.error.message}
        </p>
      )}
      {!query.isLoading && query.data?.length === 0 && (
        <p className="text-sm text-nexus-muted">No notifications recorded.</p>
      )}
      <div className="space-y-2">
        {query.data?.map((record) => {
          const status = record.delivered
            ? "Delivered"
            : record.accepted
              ? "Accepted; delivery unconfirmed"
              : record.mode === "simulated"
                ? "Simulated; not sent"
                : record.providerStatus || "Not delivered";
          return (
            <div
              key={record.id}
              className="rounded-lg border border-nexus-border p-3"
            >
              <div className="flex flex-wrap justify-between gap-2 text-xs">
                <span className="text-white">
                  {record.channel.toUpperCase()} · {record.recipient}
                </span>
                <span className={record.delivered ? "text-nexus-success" : "text-nexus-warn"}>
                  {status}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-300">{record.message}</p>
              <p className="mt-1 text-[10px] text-nexus-muted">
                {record.caseId || record.customerId || "No case"} · {record.mode} ·{" "}
                {new Date(record.createdAt).toLocaleString()}
              </p>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
