/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: [
      {
        modern: {
          "primary": "#3b82f6",
          "primary-focus": "#2563eb",
          "primary-content": "#ffffff",
          "secondary": "#8b5cf6",
          "secondary-focus": "#7c3aed",
          "secondary-content": "#ffffff",
          "accent": "#06b6d4",
          "accent-focus": "#0891b2",
          "accent-content": "#ffffff",
          "neutral": "#374151",
          "neutral-focus": "#1f2937",
          "neutral-content": "#ffffff",
          "base-100": "#ffffff",
          "base-200": "#f8fafc",
          "base-300": "#f1f5f9",
          "base-content": "#1e293b",
          "info": "#3b82f6",
          "success": "#10b981",
          "warning": "#f59e0b",
          "error": "#ef4444",
        },
      },
      "light", 
      "dark", 
      "cupcake"
    ],
  },
  plugins: [require("daisyui")],
}
