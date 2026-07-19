// Central API base URL.
// Local dev: VITE_API_URL is unset, so we fall back to the local backend.
// Production (Vercel): VITE_API_URL is set to the deployed backend URL.
export const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'