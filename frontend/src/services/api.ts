import axios from "axios";
import { API_BASE_URL } from "../lib/config";

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("nexus-token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (e) => {
    if (e?.response?.status === 401 && !e?.config?.url?.includes("/auth/login")) {
      window.dispatchEvent(new Event("nexus:unauthorized"));
    }
    const msg =
      e?.response?.data?.detail || e?.message || "Network error";
    return Promise.reject(new Error(msg));
  }
);
