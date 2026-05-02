import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#f7f9ff",
        foreground: "#181c20",
        surface: {
          DEFAULT: "#f7f9ff",
          dim: "#d7dadf",
          bright: "#f7f9ff",
          container: {
            lowest: "#ffffff",
            low: "#f1f4f9",
            DEFAULT: "#ebeef3",
            high: "#e5e8ee",
            highest: "#e0e3e8",
          },
          variant: "#e0e3e8",
        },
        primary: {
          DEFAULT: "#001e40",
          container: "#003366",
          fixed: "#d5e3ff",
        },
        secondary: {
          DEFAULT: "#005cba",
          container: "#5095fe",
          fixed: "#d7e3ff",
        },
        tertiary: {
          DEFAULT: "#181f25",
          container: "#2d343a",
          fixed: "#dce3eb",
        },
        error: {
          DEFAULT: "#ba1a1a",
          container: "#ffdad6",
        },
        outline: {
          DEFAULT: "#737780",
          variant: "#c3c6d1",
        },
        "on-primary": "#ffffff",
        "on-secondary": "#ffffff",
        "on-surface": "#181c20",
        "on-surface-variant": "#43474f",
      },
      fontFamily: {
        sans: ["var(--font-public-sans)"],
      },
      boxShadow: {
        'ambient': '0 4px 24px 0 rgba(0, 30, 64, 0.1)',
      }
    },
  },
  plugins: [],
};
export default config;
