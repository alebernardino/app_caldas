import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        base: "#070707",
        card: "#1a1a1a",
        border: "#2d2d2d",
        accent: "#f59e0b"
      }
    }
  },
  plugins: []
} satisfies Config;
