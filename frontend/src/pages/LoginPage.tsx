import { FormEvent, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { Copy, Check } from "lucide-react";
import { useAuth } from "../auth/AuthProvider";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";

const demoAccounts = [
  {
    role: "Demo Manager",
    username: "nexus_demo_manager",
    password: "Nexus-Demo-Manager-2026!",
    permissions: "View synthetic demo dashboard only. No user or production-data access.",
  },
  {
    role: "Demo Senior Agent",
    username: "nexus_demo_senior",
    password: "Nexus-Demo-Senior-2026!",
    permissions: "View synthetic demo dashboard only. No operational API access.",
  },
  {
    role: "Demo Agent",
    username: "nexus_demo_agent",
    password: "Nexus-Demo-Agent-2026!",
    permissions: "View synthetic demo dashboard only. No operational API access.",
  },
] as const;

export default function LoginPage() {
  const { user, loading, signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [copied, setCopied] = useState("");
  const [copyError, setCopyError] = useState("");

  if (loading) return <LoginFrame>Checking session…</LoginFrame>;
  if (user) return <Navigate to="/" replace />;

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const signedInUser = await signIn(username, password);
      const requestedDestination = (location.state as { from?: string } | null)?.from;
      const destination = signedInUser.role.startsWith("demo_")
        ? "/demo"
        : requestedDestination || "/";
      navigate(destination, { replace: true });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Sign-in failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <LoginFrame>
      <Card className="w-full max-w-4xl">
        <h1 className="text-xl font-semibold text-white">Sign in to NEXUS</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Secure Role-Based Access Control (RBAC) – Select Your Role and Sign In
          with Authorized Credentials.
        </p>
        <div className="mt-5 grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
          <form className="space-y-3" onSubmit={submit}>
            <h2 className="text-sm font-semibold text-white">
              Workspace sign in
            </h2>
            <label className="block text-xs text-nexus-muted">
              Username
              <input
                autoComplete="username"
                required
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                className="mt-1 w-full rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
              />
            </label>
            <label className="block text-xs text-nexus-muted">
              Password
              <input
                autoComplete="current-password"
                required
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-1 w-full rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
              />
            </label>
            {error && (
              <p role="alert" className="text-sm text-nexus-danger">
                {error}
              </p>
            )}
            <Button className="w-full" disabled={submitting}>
              {submitting ? "Signing in…" : "Sign in"}
            </Button>
          </form>
          <section aria-labelledby="demo-credentials-heading">
            <h2
              id="demo-credentials-heading"
              className="text-sm font-semibold text-white"
            >
              Demo Login Credentials – Role-Based Access
            </h2>
            <p className="mt-1 text-xs text-nexus-muted">
              These shared demo accounts are isolated from operational roles
              and can access synthetic examples only.
            </p>
            <div className="mt-3 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {demoAccounts.map((account) => (
                <div
                  key={account.username}
                  className="rounded-lg border border-nexus-border bg-nexus-bg/50 p-3"
                >
                  <h3 className="text-sm font-medium text-white">
                    {account.role}
                  </h3>
                  <p className="mt-2 text-[11px] text-nexus-muted">
                    Username
                  </p>
                  <div className="flex items-center gap-1">
                    <code className="min-w-0 flex-1 break-all text-xs text-slate-200">
                      {account.username}
                    </code>
                    <Button
                      type="button"
                      variant="ghost"
                      className="px-2 py-1"
                      aria-label={`Copy ${account.role} username`}
                      onClick={() =>
                        void copyValue(
                          `${account.role}-username`,
                          account.username,
                          setCopied,
                          setCopyError,
                        )
                      }
                    >
                      {copied === `${account.role}-username` ? (
                        <Check size={14} />
                      ) : (
                        <Copy size={14} />
                      )}
                    </Button>
                  </div>
                  <p className="mt-2 text-[11px] text-nexus-muted">
                    Password
                  </p>
                  <div className="flex items-center gap-1">
                    <code className="min-w-0 flex-1 break-all text-xs text-slate-200">
                      {account.password}
                    </code>
                    <Button
                      type="button"
                      variant="ghost"
                      className="px-2 py-1"
                      aria-label={`Copy ${account.role} password`}
                      onClick={() =>
                        void copyValue(
                          `${account.role}-password`,
                          account.password,
                          setCopied,
                          setCopyError,
                        )
                      }
                    >
                      {copied === `${account.role}-password` ? (
                        <Check size={14} />
                      ) : (
                        <Copy size={14} />
                      )}
                    </Button>
                  </div>
                  <p className="mt-2 text-[11px] leading-4 text-nexus-muted">
                    {account.permissions}
                  </p>
                  <Button
                    type="button"
                    variant="outline"
                    className="mt-3 w-full px-2 py-1 text-xs"
                    onClick={() => {
                      setUsername(account.username);
                      setPassword(account.password);
                      setError("");
                    }}
                  >
                    Use this demo account
                  </Button>
                </div>
              ))}
            </div>
            {copyError && (
              <p role="alert" className="mt-2 text-xs text-nexus-danger">
                {copyError}
              </p>
            )}
            <p className="mt-3 text-xs text-nexus-warn">
              Production Manager credentials are never displayed here.
              Administrator accounts are not a supported role.
            </p>
          </section>
        </div>
      </Card>
    </LoginFrame>
  );
}

async function copyValue(
  key: string,
  value: string,
  setCopied: (value: string) => void,
  setError: (value: string) => void,
) {
  try {
    await navigator.clipboard.writeText(value);
    setCopied(key);
    setError("");
  } catch (reason) {
    setCopied("");
    setError(
      reason instanceof Error
        ? `Could not copy to clipboard: ${reason.message}`
        : "Could not copy to clipboard.",
    );
  }
}

function LoginFrame({ children }: { children: React.ReactNode }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-nexus-bg p-4">
      {children}
    </main>
  );
}
