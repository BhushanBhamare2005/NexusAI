import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Bot,
  Search,
  ShieldCheck,
  TrendingUp,
  FileCheck,
  FlaskConical,
} from "lucide-react";
import { useAuth } from "../../auth/AuthProvider";

const links = [
  { to: "/", label: "My Dashboard", icon: LayoutDashboard, minimumRole: 0 },
  {
    to: "/command-center",
    label: "Command Center",
    icon: LayoutDashboard,
    minimumRole: 0,
  },
  { to: "/agent", label: "AI Teammate", icon: Bot, minimumRole: 0 },
  {
    to: "/demo/ai-teammate",
    label: "AI Teammate",
    icon: Bot,
    minimumRole: 0,
  },
  { to: "/transactions", label: "Transactions", icon: Search, minimumRole: 0 },
  { to: "/trustguard", label: "TrustGuard", icon: ShieldCheck, minimumRole: 1 },
  { to: "/revenue", label: "Revenue Rescue", icon: TrendingUp, minimumRole: 1 },
  { to: "/audit", label: "Evidence Center", icon: FileCheck, minimumRole: 1 },
  { to: "/demo", label: "Demo Sandbox", icon: FlaskConical, minimumRole: 0 },
];

export default function Sidebar() {
  const { user } = useAuth();
  const roleLevel = user?.role === "manager" ? 2 : user?.role === "senior_agent" ? 1 : 0;
  const visibleLinks = user?.role.startsWith("demo_")
    ? links.filter((link) =>
        ["/demo", "/demo/ai-teammate"].includes(link.to),
      )
    : links.filter(
        (link) =>
          !["/demo", "/demo/ai-teammate"].includes(link.to) &&
          roleLevel >= link.minimumRole,
      );

  return (
    <aside className="flex w-60 flex-col border-r border-nexus-border bg-nexus-panel">
      <div className="flex items-center gap-2 border-b border-nexus-border px-5 py-4">
        <div className="h-8 w-8 rounded-lg bg-nexus-accent" />
        <div>
          <div className="text-sm font-semibold text-white">NEXUS AI</div>
          <div className="text-[10px] uppercase tracking-wider text-nexus-muted">
            Autonomous Resolver
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {visibleLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/" || to === "/demo"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition ${
                isActive
                  ? "bg-nexus-accent/10 text-nexus-accent"
                  : "text-slate-300 hover:bg-white/5"
              }`
            }
          >
            <Icon size={16} />
            {to === "/trustguard" && user?.role === "manager"
              ? "Manager Dashboard"
              : label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-nexus-border p-3 text-[10px] text-nexus-muted">
        Simulated environment · No real transactions
      </div>
    </aside>
  );
}
