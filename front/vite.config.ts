import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 9000,
    allowedHosts: ["localhost", "hackbnb.dashbox.cloud"],
  },
  // [D9] Jamais de source maps dans le build de production
  build: {
    sourcemap: false,
  },
  plugins: [
    react(),
    tailwindcss(),
  ],
})
