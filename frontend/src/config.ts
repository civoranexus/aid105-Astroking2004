/// <reference types="vite/client" />

// API configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD 
    ? '/api'  // In production, use nginx proxy
    : 'http://localhost:8000'  // In development, direct to backend
  );

export const config = {
  apiUrl: API_BASE_URL,
  environment: import.meta.env.MODE,
};
