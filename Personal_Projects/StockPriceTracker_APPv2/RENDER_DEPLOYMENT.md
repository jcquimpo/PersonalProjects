# Render.com Deployment Guide

## Prerequisites
- Render.com account
- GitHub repository with this code
- Finnhub API key

## Quick Deploy Steps

### 1. Set Up Environment Variables in Render
In your Render service settings, add these environment variables:
```
FINNHUB_API_KEY=your_api_key_here
FLASK_ENV=production
```

### 2. Deploy Process
Render will automatically:
1. Install Python 3.11.8 (from `runtime.txt`)
2. Install dependencies (from `requirements.txt`)
3. Run the app with gunicorn (from `Procfile`)

### 3. Verify Deployment
After deployment, test these endpoints:
- Health check: `https://your-app.onrender.com/health`
- Home page: `https://your-app.onrender.com/`
- Dashboard: `https://your-app.onrender.com/dashboard`
- API data: `https://your-app.onrender.com/api/data`

## Fixed Issues
✅ **setuptools added** - Fixes `ModuleNotFoundError: No module named 'pkg_resources'`
✅ **pandas 2.2.0** - Pre-built wheels available, fixes build failures
✅ **gunicorn added** - Production WSGI server for Render
✅ **Procfile created** - Tells Render how to run the app
✅ **runtime.txt added** - Specifies Python 3.11.8
✅ **Debug mode disabled** - Production-safe configuration
✅ **Port from environment** - Listens on PORT env variable
✅ **Error handling improved** - Better exception handling for production

## Local Testing

### Test locally before deploying:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
set FLASK_ENV=development

# Run the app
python app.py
```

### Test with gunicorn locally:
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

## Troubleshooting

### "Build failed" error
- Check the build logs in Render dashboard
- Ensure all dependencies in `requirements.txt` are compatible
- Try rebuilding from scratch

### "ModuleNotFoundError"
- ✅ Fixed by adding `setuptools` to requirements.txt

### "Failed to build 'pandas'"
- ✅ Fixed by updating to pandas 2.2.0 (has pre-built wheels)

### API errors
- Verify FINNHUB_API_KEY is set in Render environment
- Check Render logs for API rate limiting messages
- Ensure network connectivity to external APIs

### Port issues
- Render automatically assigns a port via PORT environment variable
- The app now reads from `os.getenv("PORT", 5000)`
- This is handled automatically by gunicorn

## Performance Notes
- Connection pooling enabled (10 connections)
- Retry logic with exponential backoff
- 2-second delay between API calls to respect rate limits
- Proper error handling and validation

## Next Steps
1. Push code to GitHub (if not already done)
2. Connect your GitHub repo to Render
3. Set environment variables in Render
4. Deploy and monitor the service
