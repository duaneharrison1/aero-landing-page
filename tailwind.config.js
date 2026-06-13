/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "'Segoe UI'", "Roboto", "sans-serif"],
      },
      colors: {
        accent: {
          DEFAULT: "#3D78B0",
          hover: "#2F6499",
          tint: "rgba(61,120,176,0.08)",
          focus: "rgba(61,120,176,0.14)",
        },
        page: "#FFFFFF",
        surface: {
          DEFAULT: "#F4F5F8",
          secondary: "#F9FAFB",
        },
        text: {
          primary: "#1D1D1F",
          secondary: "#6B6F76",
          muted: "#8E8E93",
        },
      },
      borderRadius: {
        sm: "6px",
        DEFAULT: "8px",
      },
      boxShadow: {
        card: "0 2px 8px rgba(0,0,0,0.06)",
        dropdown: "0 4px 12px rgba(0,0,0,0.08)",
        btn: "0 2px 8px rgba(61,120,176,0.15)",
        glass: "0 16px 48px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
