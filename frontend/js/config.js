// Frontend runtime config - allows overriding API base URL at deploy time.
// On Vercel, backend and frontend share the same origin, so we use a relative path.
// For local development it falls back to localhost:5000.
const _isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
window.API_BASE_URL = window.__API_BASE_URL__ || (_isLocal ? 'http://localhost:5000/api' : '/api');
