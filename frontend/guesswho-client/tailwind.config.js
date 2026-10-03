/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{vue,js}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        board: "#1156fc", // the blue plastic board
        tray: "#0a2a8a", // shadowed blue behind panels
        zap: "#e0e300", // yellow for actions and selection
        plate: "#d62828", // red name plates on the cards
      },
      fontFamily: {
        display: ["Bangers", "sans-serif"],
        body: ["Rubik", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
