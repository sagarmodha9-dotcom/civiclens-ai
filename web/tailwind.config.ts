import type { Config } from "tailwindcss";
export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: { 950: "#0a0d12", 900: "#0f131a", 850: "#131924", 800: "#182030", 700: "#243044", 600: "#34435c" },
        mist: { 50: "#f3f5f8", 100: "#e6eaf0", 300: "#b8c2d1", 400: "#8f9bb0", 500: "#8592a8" },
        signal: { DEFAULT: "#5aa9ff", soft: "#8cc3ff" },
        amber: { DEFAULT: "#f2b544" },
        rose: { DEFAULT: "#ff6b7a" },
        mint: { DEFAULT: "#4cd090" },
      },
      fontFamily: { sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "sans-serif"], mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"] },
      boxShadow: { panel: "0 1px 0 0 rgba(255,255,255,0.04) inset, 0 8px 24px -16px rgba(0,0,0,0.6)" },
    },
  },
  plugins: [],
} satisfies Config;
