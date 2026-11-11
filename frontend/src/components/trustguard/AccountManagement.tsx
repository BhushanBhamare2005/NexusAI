import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";

type Role =
  | "manager"
  | "senior_agent"
  | "agent"
  | "demo_manager"
  | "demo_senior_agent"
  | "demo_agent";

interface WorkspaceUser {
  id: string;
  username: string;
  role: Role;
  is_active: boolean;
  is_demo: boolean;
  created_at: string;
}

interface RoleHistoryEntry {
  id: string;
  target_username: string;
  actor_username: string;
  action: string;
  previous_role: Role | null;
  new_role: Role | null;
  previous_active: boolean | null;
  new_active: boolean | null;
  created_at: string;
}

export default function AccountManagement() {
  const queryClient = useQueryClient();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("agent");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const users = useQuery({
    queryKey: ["workspace-users"],
    queryFn: async () => (await api.get<WorkspaceUser[]>("/auth/users")).data,
  });
  const history = useQuery({
    queryKey: ["role-assignment-history"],
    queryFn: async () =>
      (await api.get<RoleHistoryEntry[]>("/auth/role-history")).data,
  });
  const updateUser = useMutation({
    mutationFn: async ({
      userId,
      update,
    }: {
      userId: string;
      update: { role?: Role; is_active?: boolean };
    }) => api.patch(`/auth/users/${userId}`, update),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["workspace-users"] }),
        queryClient.invalidateQueries({ queryKey: ["role-assignment-history"] }),
        queryClient.invalidateQueries({ queryKey: ["auth-user"] }),
      ]);
    },
  });

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
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["workspace-users"] }),
        queryClient.invalidateQueries({ queryKey: ["role-assignment-history"] }),
      ]);
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
            <option value="demo_agent">Demo agent (restricted)</option>
            <option value="demo_senior_agent">Demo senior agent (restricted)</option>
            <option value="demo_manager">Demo manager (restricted)</option>
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
      <div className="mt-6">
        <CardTitle>Workspace users and roles</CardTitle>
        {users.isLoading && (
          <p className="text-sm text-nexus-muted">Loading users…</p>
        )}
        {users.isError && (
          <p role="alert" className="text-sm text-nexus-danger">
            Could not load users: {users.error.message}
          </p>
        )}
        {updateUser.isError && (
          <p role="alert" className="mb-2 text-sm text-nexus-danger">
            Could not update account: {updateUser.error.message}
          </p>
        )}
        <div className="space-y-2">
          {users.data?.map((user) => (
            <div
              key={user.id}
              className="flex flex-wrap items-center gap-3 rounded-lg border border-nexus-border p-3"
            >
              <div className="min-w-[150px] flex-1">
                <div className="text-sm text-white">{user.username}</div>
                <div className="text-xs text-nexus-muted">
                  {user.id} · {user.is_active ? "Active" : "Inactive"}
                  {user.is_demo ? " · Isolated demo account" : ""}
                </div>
              </div>
              <label className="text-xs text-nexus-muted">
                Role
                <select
                  aria-label={`Role for ${user.username}`}
                  value={user.role}
                  disabled={updateUser.isPending}
                  onChange={(event) =>
                    updateUser.mutate({
                      userId: user.id,
                      update: { role: event.target.value as Role },
                    })
                  }
                  className="ml-2 rounded-lg border border-nexus-border bg-nexus-bg px-2 py-2 text-sm text-white"
                >
                  <option value="manager">Manager</option>
                  <option value="senior_agent">Senior Agent</option>
                  <option value="agent">Agent</option>
                  {user.is_demo && (
                    <>
                      <option value="demo_manager">Demo Manager</option>
                      <option value="demo_senior_agent">Demo Senior Agent</option>
                      <option value="demo_agent">Demo Agent</option>
                    </>
                  )}
                </select>
              </label>
              <Button
                variant={user.is_active ? "danger" : "outline"}
                disabled={updateUser.isPending}
                onClick={() =>
                  updateUser.mutate({
                    userId: user.id,
                    update: { is_active: !user.is_active },
                  })
                }
              >
                {user.is_active ? "Deactivate" : "Activate"}
              </Button>
            </div>
          ))}
        </div>
      </div>
      <div className="mt-6">
        <CardTitle>Role assignment history</CardTitle>
        {history.isLoading && (
          <p className="text-sm text-nexus-muted">Loading history…</p>
        )}
        {history.isError && (
          <p role="alert" className="text-sm text-nexus-danger">
            Could not load role history: {history.error.message}
          </p>
        )}
        <div className="max-h-64 space-y-2 overflow-y-auto">
          {history.data?.map((entry) => (
            <div
              key={entry.id}
              className="rounded-lg border border-nexus-border p-3 text-xs text-nexus-muted"
            >
              <div className="text-slate-200">
                {entry.action.replaceAll("_", " ")} · {entry.target_username}
              </div>
              <div>
                By {entry.actor_username}
                {entry.previous_role && entry.new_role
                  ? ` · ${entry.previous_role.replace("_", " ")} → ${entry.new_role.replace("_", " ")}`
                  : entry.new_role
                    ? ` · assigned ${entry.new_role.replace("_", " ")}`
                    : ""}
                {entry.previous_active !== null && entry.new_active !== null
                  ? ` · ${entry.previous_active ? "active" : "inactive"} → ${entry.new_active ? "active" : "inactive"}`
                  : ""}
              </div>
              <div>{new Date(entry.created_at).toLocaleString()}</div>
            </div>
          ))}
          {history.data?.length === 0 && (
            <p className="text-sm text-nexus-muted">No role changes recorded.</p>
          )}
        </div>
      </div>
    </Card>
  );
}
