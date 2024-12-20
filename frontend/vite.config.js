import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  publicDir: 'public',  // Directorio donde se encuentra index.html
  build: {
    outDir: 'dist',  // Directorio de salida
    rollupOptions: {
      input: 'public/index.html'  // Asegúrate de que apunta correctamente a index.html
    }
  }
});
