import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        "deep-ink": "#111827",
        parchment: "#F8F4EA",
        ivory: "#FFFDF7",
        "gavel-gold": "#D4A017",
        "verdict-teal": "#0F766E",
        "objection-amber": "#F59E0B",
        "overruled-red": "#B91C1C",
        "dark-red": "#7F1D1D",
        charcoal: "#1F2937",
        "slate-gray": "#6B7280",
        "paper-line": "#D6D3C8",
      },
    },
  },
  plugins: [],
};

export default config;
