import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The API runs on API_PORT (default 8000); the dev server proxies /api to it.
const apiPort = process.env.API_PORT ?? '8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: Number(process.env.PORT ?? 5173),
    proxy: { '/api': `http://localhost:${apiPort}` },
  },
})
