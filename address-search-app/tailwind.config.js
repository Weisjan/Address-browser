/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ["Montserrat", "Arial", "sans-serif"],
      },
      boxShadow: {
        custom: "0 0 10px grey",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
