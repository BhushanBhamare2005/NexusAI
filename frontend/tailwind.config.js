/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        nexus: {
          bg: "#0B1220",
          panel: "#111C33",
          border: "#1E2D4A",
          accent: "#00B9F1",
          success: "#22C55E",
          warn: "#F59E0B",
          danger: "#EF4444",
          muted: "#94A3B8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
