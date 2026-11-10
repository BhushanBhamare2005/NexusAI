import { FormEvent, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";

export default function LoginPage() {
  const { user, loading, signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (loading) return <LoginFrame>Checking session…</LoginFrame>;
  if (user) return <Navigate to="/" replace />;

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await signIn(username, password);
      const destination = (location.state as { from?: string } | null)?.from || "/";
      navigate(destination, { replace: true });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Sign-in failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <LoginFrame>
      <Card className="w-full max-w-md">
        <h1 className="text-xl font-semibold text-white">Sign in to NEXUS</h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Use your workspace account. Passwords are stored as bcrypt hashes.
        </p>
        <form className="mt-5 space-y-3" onSubmit={submit}>
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
        <p className="mt-4 text-xs text-nexus-muted">
          First run? Configure NEXUS_BOOTSTRAP_USERNAME and
          NEXUS_BOOTSTRAP_PASSWORD before starting the API.
        </p>
      </Card>
    </LoginFrame>
  );
}

function LoginFrame({ children }: { children: React.ReactNode }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-nexus-bg p-4">
      {children}
    </main>
  );
}
