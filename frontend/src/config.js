// API Configuration
// Automatically uses the correct backend URL based on environment

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('🌐 API Base URL:', API_BASE_URL);
