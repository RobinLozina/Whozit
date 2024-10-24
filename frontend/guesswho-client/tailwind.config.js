/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ["./src/**/*.{vue,js,ts,jsx,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        futura: ["FuturaPT", "sans-serif"],
        bangers: ["Bangers", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
