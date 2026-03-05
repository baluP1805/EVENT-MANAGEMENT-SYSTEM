/**
 * Frontend Utility Functions
 * Security and helper functions for the College EMS application
 */

/**
 * Escape HTML special characters to prevent XSS
 * Use this when inserting user-provided content into the DOM
 * @param {string} text - The text to escape
 * @returns {string} - HTML-safe text
 */
function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    };
    
    return text.replace(/[&<>"'/]/g, char => map[char]);
}

/**
 * Sanitize object properties for safe HTML rendering
 * @param {object} obj - Object to sanitize
 * @param {array} fields - Array of field names to sanitize
 * @returns {object} - Object with sanitized fields
 */
function sanitizeObject(obj, fields) {
    const sanitized = { ...obj };
    fields.forEach(field => {
        if (sanitized[field]) {
            sanitized[field] = escapeHtml(sanitized[field]);
        }
    });
    return sanitized;
}

/**
 * Validate JWT token format
 * @param {string} token - JWT token to validate
 * @returns {boolean} - True if valid format
 */
function isValidJWTFormat(token) {
    if (!token || typeof token !== 'string') return false;
    const parts = token.split('.');
    return parts.length === 3;
}

/**
 * Format date for display
 * @param {string} dateString - Date string to format
 * @returns {string} - Formatted date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Format time for display
 * @param {string} dateString - Date string to format
 * @returns {string} - Formatted time
 */
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Show a temporary notification message
 * @param {string} message - Message to display
 * @param {string} type - Type of message ('success', 'error', 'info')
 * @param {number} duration - Duration in milliseconds (default: 3000)
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

/**
 * Debounce function to limit execution rate
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Check if user is authenticated (has valid token)
 * @returns {boolean} - True if authenticated
 */
function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token && isValidJWTFormat(token);
}

/**
 * Get token from localStorage
 * @returns {string|null} - Token or null
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Logout user (clear token and redirect)
 * @param {string} redirectTo - URL to redirect to after logout
 */
function logout(redirectTo = '/pages/login.html') {
    localStorage.removeItem('token');
    localStorage.removeItem('studentId');
    window.location.href = redirectTo;
}
