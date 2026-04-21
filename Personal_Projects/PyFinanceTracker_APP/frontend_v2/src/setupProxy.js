/**
 * HTTP Proxy Middleware Setup for Development
 * This proxies API calls from localhost:3000/api to localhost:5000/api
 * Allows frontend and backend to run on different ports during development
 */

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api',
      },
      onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).json({
          error: 'Backend API is not accessible',
          message: err.message,
        });
      },
    })
  );
};
