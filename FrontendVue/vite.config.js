import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/auth': 'http://127.0.0.1:5000',
      '/admin': 'http://127.0.0.1:5000',
      '/staff': 'http://127.0.0.1:5000',
      '/user': 'http://127.0.0.1:5000',
      '/api': 'http://127.0.0.1:5000',
      '/static/exports': 'http://127.0.0.1:5000'
    }
  }
});
