# GitHub Pages & Deployment Checklist

## Pre-Deployment Checklist

### Code Quality
- [ ] All Python files have no syntax errors
- [ ] JavaScript console has no errors
- [ ] `.env` file is in `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] All dependencies in `requirements.txt`

### Files Created for GitHub
- [x] `.gitignore` - Excludes sensitive files
- [x] `Procfile` - For Heroku deployment
- [x] `runtime.txt` - Python version specification
- [x] `.env.example` - Environment variables template
- [x] `requirements.txt` - Updated with gunicorn and flask-cors
- [x] `.github/workflows/deploy-pages.yml` - GitHub Actions workflow
- [x] `static/config.js` - API configuration
- [x] `DEPLOYMENT.md` - Deployment instructions
- [x] `GITHUB_SETUP.md` - GitHub setup guide

### Flask Configuration
- [x] CORS enabled in `flask_app.py`
- [x] Environment variable support
- [x] Error handling for API endpoints
- [x] Logging configured

---

## Step 1: Prepare Local Repository

```bash
cd d:\VSCode_Projs\PersonalProjects\Personal_Projects\StockPriceTracker_APPv2

# Initialize git
git init
git add .
git commit -m "Initial commit: Stock Price Tracker App ready for GitHub"

# Verify everything is committed
git status
```

**Expected Output:** `On branch main, working tree clean`

---

## Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository Name:** `StockPriceTracker-APPv2`
3. **Description:** Real-time stock analysis dashboard with Flask backend
4. **Visibility:** Public (so GitHub Pages can deploy)
5. **Initialize:** Leave unchecked (we already have local repo)
6. Click **Create repository**

---

## Step 3: Push to GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2.git
git push -u origin main
```

**Verify:** Check GitHub - you should see all your files

---

## Step 4: Enable GitHub Pages

1. Go to your repository → **Settings**
2. Click **Pages** (left sidebar)
3. **Source:** Select "GitHub Actions"
4. Wait a few seconds for the workflow to run
5. Your site URL: `https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2`

**Verify:** Visit the URL - should see the dashboard

---

## Step 5: Deploy Backend (Choose One)

### Option A: Heroku (Recommended for Beginners)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create stocktracker-yourname

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set FINNHUB_API_KEY=your_key_here

# Deploy
git push heroku main

# Monitor
heroku logs --tail
```

**Backend URL:** `https://stocktracker-yourname.herokuapp.com`

### Option B: PythonAnywhere (Free & Simple)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create new Web app
3. Clone this repo: `git clone https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2.git`
4. Set WSGI file to point to `flask_app.py:app`
5. Install requirements in Bash console
6. Reload app

**Backend URL:** `https://yourname.pythonanywhere.com`

### Option C: Railway (Easiest - Just Push)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect GitHub and select your repository
4. Add environment variable: `FINNHUB_API_KEY=your_key`
5. Railway auto-deploys on push

**Backend URL:** Provided in Railway dashboard

---

## Step 6: Connect Frontend to Backend

**Update `static/config.js`:**

Find this line:
```javascript
return 'https://your-backend-url-here.com';
```

Replace with your backend URL:
- **Heroku:** `https://stocktracker-yourname.herokuapp.com`
- **PythonAnywhere:** `https://yourname.pythonanywhere.com`
- **Railway:** Your Railway URL

Then push:
```bash
git add static/config.js
git commit -m "Update API URL for backend"
git push origin main
```

---

## Step 7: Test Integration

### Test Frontend
- [ ] Visit `https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2`
- [ ] Page loads without errors
- [ ] Layout looks correct

### Test Backend
- [ ] Visit `https://your-backend.com/api/status` (replace with your URL)
- [ ] Should return JSON: `{"is_running": false, "has_results": false, ...}`

### Test Integration
- [ ] Click "Run Analysis"
- [ ] Check browser console (F12) for errors
- [ ] Analysis should complete in 2-5 minutes
- [ ] Tables should populate with data
- [ ] Charts should render

---

## Step 8: Share Your Project!

### Add GitHub Badge to README

```markdown
## Deployment Status

[![GitHub Pages Deployment](https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2/actions)

**Live Site:** https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2
**Backend:** https://your-backend.com
```

### Share Links
- Repository: `https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2`
- Live Site: `https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2`

---

## Troubleshooting

### GitHub Pages showing 404
- [ ] Check Settings → Pages
- [ ] Verify GitHub Actions workflow succeeded
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Wait 5 minutes for propagation

### Backend API returning 404
- [ ] Verify backend is running/deployed
- [ ] Check backend URL in `static/config.js`
- [ ] Visit backend directly: `https://your-backend/api/status`
- [ ] Check backend logs

### CORS Errors
- [ ] Already enabled in `flask_app.py`
- [ ] If still errors, check backend logs
- [ ] Ensure frontend URL is added to CORS origins

### Analysis Times Out
- [ ] Heroku free tier may be slow
- [ ] Upgrade to paid tier or use Railway
- [ ] Check backend logs for API rate limiting
- [ ] Increase timeout in code

### Missing Dependencies
- [ ] Run: `pip install -r requirements.txt`
- [ ] On Heroku: `heroku run pip install -r requirements.txt`
- [ ] On PythonAnywhere: Use Bash console

---

## After Deployment

### Keep Code Updated

```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push origin main

# This triggers:
# 1. GitHub Actions for frontend
# 2. Auto-deploy on Railway/Heroku
```

### Monitor Backend

```bash
# Heroku logs
heroku logs --tail

# Django/Flask errors
# Check PYTHONUNBUFFERED=1 for output
```

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update in requirements.txt
pip install --upgrade package-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

---

## Useful Commands Reference

```bash
# Local Development
python flask_app.py                    # Run locally
python -m pip install -r requirements.txt  # Install deps

# Git
git status                             # Check changes
git add .                              # Stage all
git commit -m "message"                # Commit
git push origin main                   # Push to GitHub

# Heroku
heroku logs --tail                     # View logs
heroku config                          # View environment vars
heroku restart                         # Restart app
heroku open                            # Open app in browser

# PythonAnywhere
# Use bash console in Web app settings

# Railway
# Use Railway CLI or dashboard at https://railway.app
```

---

## Getting Help

- 📚 [GitHub Pages Docs](https://docs.github.com/en/pages)
- 🚀 [Heroku Deployment Guide](https://devcenter.heroku.com/articles/deploying-python-apps-on-heroku)
- 🐍 [PythonAnywhere Help](https://help.pythonanywhere.com/)
- 🛤️ [Railway Docs](https://docs.railway.app/)
- 🍶 [Flask Documentation](https://flask.palletsprojects.com/)

---

**All set! Your app should now be live on GitHub Pages with a backend running on your chosen platform.**
