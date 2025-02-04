/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "../templates/**/*.html",
    "../**/templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
