/**
 * Application Configuration
 * 
 * Update API_BASE_URL based on your deployment environment:
 * 
 * LOCAL DEVELOPMENT:
 *   API_BASE_URL = 'http://localhost:5000'
 * 
 * HEROKU:
 *   API_BASE_URL = 'https://your-app-name.herokuapp.com'
 * 
 * PYTHONANYWHERE:
 *   API_BASE_URL = 'https://yourusername.pythonanywhere.com'
 * 
 * RAILWAY:
 *   API_BASE_URL = 'https://your-railway-url.up.railway.app'
 * 
 * GITHUB PAGES + EXTERNAL BACKEND:
 *   API_BASE_URL = 'https://your-backend-url.com'
 */

// Determine API base URL based on environment
window.API_CONFIG = {
    BASE_URL: (() => {
        // Check if running locally
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:5000';
        }
        
        // Check if running on GitHub Pages
        if (window.location.hostname.includes('github.io')) {
            // UPDATE THIS with your backend URL
            return 'https://your-backend-url-here.com';
        }
        
        // Default to same domain
        return window.location.origin;
    })(),

    // Enable debug logging
    DEBUG: window.location.hostname === 'localhost'
};

// Log configuration on page load
console.log('📡 API Config:', window.API_CONFIG);
