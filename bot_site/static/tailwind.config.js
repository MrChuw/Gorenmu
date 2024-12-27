/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/*.html", "../templates/**/*.html"],
  theme: {
    extend: {
      gridTemplateColumns: {
      'auto-fill-100': 'repeat(auto-fill, minmax(min(100px, 100%), 1fr))',
      'auto-fit-100': 'repeat(auto-fit, minmax(min(100px, 100%), 1fr))',
    },},
  },
  plugins: [],
}

