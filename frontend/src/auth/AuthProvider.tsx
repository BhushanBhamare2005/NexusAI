import {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { api } from "../services/api";

export interface AuthUser {
  username: string;
  role: "agent" | "senior_agent" | "manager";
}

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleUnauthorized = () => {
      localStorage.removeItem("nexus-token");
      setUser(null);
    };
    window.addEventListener("nexus:unauthorized", handleUnauthorized);

    const token = localStorage.getItem("nexus-token");
    if (!token) {
      setLoading(false);
    } else {
      api
        .get<AuthUser>("/auth/me")
        .then(({ data }) => setUser(data))
        .catch(() => setUser(null))
        .finally(() => setLoading(false));
    }

    return () =>
      window.removeEventListener("nexus:unauthorized", handleUnauthorized);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      async signIn(username, password) {
        const { data } = await api.post<{ token: string; user: AuthUser }>(
          "/auth/login",
          { username, password },
        );
        localStorage.setItem("nexus-token", data.token);
        setUser(data.user);
      },
      signOut() {
        localStorage.removeItem("nexus-token");
        setUser(null);
      },
    }),
    [loading, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
