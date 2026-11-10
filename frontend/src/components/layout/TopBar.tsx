import { Activity } from "lucide-react";
import { useAuth } from "../../auth/AuthProvider";
import { Button } from "../ui/button";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../services/api";

export default function TopBar() {
  const { user, signOut } = useAuth();
  const health = useQuery({
    queryKey: ["health"],
    queryFn: async () => (await api.get<{ status: string }>("/health")).data,
    refetchInterval: 15000,
    retry: false,
  });
  return (
    <header className="flex items-center justify-between border-b border-nexus-border bg-nexus-panel px-6 py-3">
      <div className="flex items-center gap-2 text-sm text-nexus-muted">
        <span>Merchant Operations</span>
        <span className="rounded-full bg-nexus-warn/15 px-2 py-0.5 text-[10px] font-medium text-nexus-warn">
          SIMULATION · Payments are not real
        </span>
      </div>
      <div className="flex items-center gap-2 text-xs">
        <span className="text-nexus-muted">
          {user?.username} · {user?.role.replace("_", " ")}
        </span>
        <Activity
          size={14}
          className={health.isError ? "text-nexus-danger" : "text-nexus-success"}
        />
        <span className={health.isError ? "text-nexus-danger" : "text-nexus-success"}>
          {health.isError ? "API unavailable" : "API connected"}
        </span>
        <Button className="px-2 py-1 text-xs" variant="ghost" onClick={signOut}>
          Sign out
        </Button>
      </div>
    </header>
  );
}
