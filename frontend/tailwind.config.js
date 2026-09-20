/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#1E2761',
          800: '#162054',
        },
        teal: {
          DEFAULT: '#028090',
          600: '#006d7b',
        },
      },
    },
  },
  plugins: [],
};
