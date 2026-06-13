/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
      colors: {
        accent: {
          DEFAULT: "#3D78B0",
          hover: "#2F6499",
          tint: "rgba(61,120,176,0.08)",
          focus: "rgba(61,120,176,0.14)",
        },
        aero: {
          bg: "#FFFFFF",
          secondary: "#F9FAFB",
          surface: "#F4F5F8",
          text: "#1D1D1F",
          "text-secondary": "#6B6F76",
          muted: "#8E8E93",
        },
      },
      borderColor: {
        subtle: "rgba(0,0,0,0.06)",
      },
      borderRadius: {
        sm: "6px",
        DEFAULT: "6px",
        lg: "8px",
      },
      boxShadow: {
        dropdown: "0 4px 12px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
