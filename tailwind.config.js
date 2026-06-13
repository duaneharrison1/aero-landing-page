/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "DM Sans Variable",
          "DM Sans",
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
      },
      colors: {
        accent: {
          DEFAULT: "#5B6DC2",
          hover: "#4D5DA5",
          tint: "#EEF1FB",
        },
        ink: "#16181F",
      },
    },
  },
  plugins: [],
};
