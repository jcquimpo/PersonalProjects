# Deployment Guide

This project consists of:
- **Frontend**: Static HTML/CSS/JS (deployable to GitHub Pages)
- **Backend**: Flask Python application (requires external hosting)

## Option 1: Deploy Backend to Heroku (Recommended for beginners)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps

1. **Create Heroku app:**
```bash
heroku login
heroku create your-app-name
```

2. **Add Python buildpack:**
```bash
heroku buildpacks:set heroku/python
```

3. **Set environment variables (if needed):**
```bash
heroku config:set DEBUG=False
```

4. **Deploy:**
```bash
git push heroku main
```

5. **View logs:**
```bash
heroku logs --tail
```

Your app will be available at: `https://your-app-name.herokuapp.com`

---

## Option 2: Deploy Backend to PythonAnywhere

### Prerequisites
- PythonAnywhere account (free tier available)
- Git installed

### Steps

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create account and open Web tab
3. Click "Add a new web app"
4. Choose "Manual configuration" → Python 3.9+
5. In "Source code" section:
```bash
git clone https://github.com/yourusername/your-repo.git /home/yourusername/mysite
```

6. Configure WSGI file to point to `flask_app.py:app`
7. Install dependencies:
```bash
pip install -r requirements.txt
```

8. Click "Reload" to restart the app

Your app will be available at: `https://yourusername.pythonanywhere.com`

---

## Option 3: Deploy Backend to Railway

### Prerequisites
- Railway account (free tier available)
- Project on GitHub

### Steps

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select this repository
5. Railway will auto-detect Flask app
6. Deploy is automatic on git push

Your app will be available at the Railway-provided URL

---

## Updating Frontend on GitHub Pages

### Using GitHub Actions (Automated)

1. **Create `.github/workflows/deploy.yml`** (provided)
2. **Enable GitHub Pages:**
   - Go to Settings → Pages
   - Select "GitHub Actions" as source
   - Deploy will run automatically on push

### Manual Deployment

```bash
# Build if needed
npm run build  # or your build command

# Push to main branch
git push origin main

# GitHub Pages will auto-update from main or gh-pages branch
```

---

## Frontend Configuration for Different Backends

Update API URLs in `static/main.js`:

```javascript
// For local development
const API_BASE = 'http://localhost:5000';

// For Heroku
const API_BASE = 'https://your-app-name.herokuapp.com';

// For PythonAnywhere
const API_BASE = 'https://yourusername.pythonanywhere.com';
```

Or set via environment variable and use in API calls:
```javascript
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

---

## CORS Configuration

The Flask backend needs to allow requests from GitHub Pages domain:

```python
# flask_app.py
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourusername.github.io", "http://localhost:5000"]
    }
})
```

Install CORS:
```bash
pip install flask-cors
```

---

## Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run Flask app:**
```bash
python flask_app.py
```

3. **Open browser:**
```
http://localhost:5000
```

---

## Troubleshooting

### CORS Errors
- Check Flask backend has CORS enabled
- Verify frontend API URL matches backend domain

### API 404 Errors
- Confirm Flask app is running
- Check backend logs for errors
- Verify API endpoints exist in flask_app.py

### Analysis Timeouts
- May need to upgrade hosting tier
- Consider caching analysis results
- Add rate limiting to yfinance calls
