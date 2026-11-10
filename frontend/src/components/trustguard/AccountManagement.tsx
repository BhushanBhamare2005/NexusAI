import { FormEvent, useState } from "react";
import { api } from "../../services/api";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";

export default function AccountManagement() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("agent");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage("");
    setError("");
    setSubmitting(true);
    try {
      await api.post("/auth/users", { username, password, role });
      setMessage(`Created ${role.replace("_", " ")} account "${username}".`);
      setUsername("");
      setPassword("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Account creation failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardTitle>Create workspace account</CardTitle>
      <p className="mb-3 text-xs text-nexus-muted">
        New passwords must be at least 12 characters. Passwords are stored as
        salted bcrypt hashes.
      </p>
      <form className="grid gap-3 md:grid-cols-3" onSubmit={submit}>
        <input
          required
          minLength={3}
          maxLength={80}
          pattern="[a-zA-Z0-9_.-]+"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          placeholder="Username"
          autoComplete="off"
          className="rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
        />
        <input
          required
          minLength={12}
          maxLength={72}
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Temporary password"
          autoComplete="new-password"
          className="rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
        />
        <div className="flex gap-2">
          <select
            value={role}
            onChange={(event) => setRole(event.target.value)}
            className="min-w-0 flex-1 rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
          >
            <option value="agent">Agent</option>
            <option value="senior_agent">Senior agent</option>
            <option value="manager">Manager</option>
          </select>
          <Button disabled={submitting}>Create</Button>
        </div>
      </form>
      {message && <p className="mt-3 text-sm text-nexus-success">{message}</p>}
      {error && (
        <p role="alert" className="mt-3 text-sm text-nexus-danger">
          {error}
        </p>
      )}
    </Card>
  );
}
