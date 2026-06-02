/**
 * React Application Entry Point
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css';

// Handle external messages from Chrome extensions
// This prevents "A listener indicated an asynchronous response by returning true" errors
if (window.chrome && window.chrome.runtime) {
  window.chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    try {
      // Log message for debugging (in case we need to handle specific extensions)
      if (request && request.action) {
        console.debug('[Extension Message]', request.action);
      }
      // Always respond to prevent unhandled async errors
      sendResponse({ status: 'received' });
    } catch (err) {
      // Silently ignore any errors in extension communication
      console.debug('[Extension Message Error]', err.message);
    }
    // Return false to indicate we handled the response synchronously
    return false;
  });
}

// Handle unhandled promise rejections from external sources
window.addEventListener('unhandledrejection', (event) => {
  // Suppress errors that are likely from browser extensions
  if (
    event.reason &&
    event.reason.message &&
    (event.reason.message.includes('message channel') ||
      event.reason.message.includes('port closed') ||
      event.reason.message.includes('Extension context invalidated'))
  ) {
    console.debug('[Extension Communication Error - Suppressed]', event.reason.message);
    event.preventDefault();
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
