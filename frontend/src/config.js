// API Configuration
// Automatically uses the correct backend URL based on environment

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('🌐 API Base URL:', API_BASE_URL);
