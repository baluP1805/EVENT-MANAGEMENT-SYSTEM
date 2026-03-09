// Frontend runtime config - allows overriding API base URL at deploy time
// Set `window.__API_BASE_URL__` in your hosting platform to point to the backend URL
window.API_BASE_URL = window.__API_BASE_URL__ || 'http://localhost:5000/api';
