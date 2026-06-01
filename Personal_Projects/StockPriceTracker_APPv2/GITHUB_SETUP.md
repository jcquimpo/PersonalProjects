# GitHub Setup Guide

## Quick Start

### 1. Initialize Git Repository

```bash
cd d:\VSCode_Projs\PersonalProjects\Personal_Projects\StockPriceTracker_APPv2

# Initialize git
git init
git add .
git commit -m "Initial commit: Stock Price Tracker App"
```

### 2. Create Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `StockPriceTracker-APPv2` (or your preference)
3. Description: "Real-time stock analysis dashboard with Flask backend"
4. Click "Create repository"

### 3. Connect Local to GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/StockPriceTracker-APPv2.git
git push -u origin main
```

---

## Enable GitHub Pages

### Option A: Deploy Static Frontend Only (Recommended)

1. **Go to Repository Settings**
   - Click Settings → Pages
   - Select "Deploy from a branch" (if available)
   - Choose branch: `main`
   - Choose folder: `/ (root)` or `/docs`

2. **Your site will be published at:**
   ```
   https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2
   ```

### Option B: Using GitHub Actions (Automated Deployment)

1. GitHub Actions workflow already configured (`.github/workflows/deploy-pages.yml`)
2. Go to Settings → Pages
3. Select "GitHub Actions" as source
4. Workflow runs automatically on push

---

## Deploy Flask Backend

Choose one platform:

### Heroku (Free with card on file)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create stockpricetracker-yourname

# Push code
git push heroku main

# View logs
heroku logs --tail
```

**Backend URL:** `https://stockpricetracker-yourname.herokuapp.com`

### PythonAnywhere (Free tier)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Create new web app
4. Configure with this repo URL
5. Install requirements in their console
6. Reload app

**Backend URL:** `https://yourname.pythonanywhere.com`

### Railway (Easiest setup)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect GitHub and select this repo
4. Auto-deploys on every push

**Backend URL:** Railway provides it

---

## Connect Frontend to Backend

### Update API URL in `static/main.js`

```javascript
// For local development
const API_BASE = 'http://localhost:5000';

// For Heroku
const API_BASE = 'https://stockpricetracker-yourname.herokuapp.com';

// For PythonAnywhere
const API_BASE = 'https://yourname.pythonanywhere.com';

// For Railway
const API_BASE = 'https://your-railway-url.up.railway.app';
```

Or add to `templates/dashboard.html`:

```javascript
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://your-deployed-backend.com';
```

---

## File Structure for Deployment

```
StockPriceTracker-APPv2/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml          # GitHub Actions workflow
├── .gitignore                        # Files to ignore in git
├── templates/                         # Frontend HTML
│   ├── base.html
│   ├── index.html
│   └── dashboard.html
├── static/                           # Frontend CSS/JS
│   ├── main.js
│   └── style.css
├── public/                           # Static assets
├── flask_app.py                      # Flask backend
├── StockPriceTracker_appv2.py        # Analysis engine
├── requirements.txt                  # Python dependencies
├── Procfile                          # Heroku deployment config
├── runtime.txt                       # Python version for Heroku
├── README.md                         # Project documentation
├── DEPLOYMENT.md                     # Deployment guide
└── GITHUB_SETUP.md                   # This file
```

---

## Environment Variables

### For GitHub Secrets (CI/CD)

Go to Settings → Secrets and variables → Actions → New repository secret

```
FINNHUB_API_KEY=your_api_key_here
```

Use in GitHub Actions:
```yaml
env:
  FINNHUB_API_KEY: ${{ secrets.FINNHUB_API_KEY }}
```

### For Heroku

```bash
heroku config:set FINNHUB_API_KEY=your_api_key
```

### For PythonAnywhere

Set in Web app configuration or `.env` file

### For Railway

Add in project variables dashboard

---

## Update .gitignore

Already configured to exclude:
- `__pycache__/`
- `.env` (secrets)
- `venv/` (local environment)
- `.DS_Store` (OS files)

---

## Verify Deployment

1. **Frontend (GitHub Pages):**
   - Visit `https://YOUR_USERNAME.github.io/StockPriceTracker-APPv2`
   - Should see landing page

2. **Backend:**
   - Verify backend URL is accessible
   - Check `/api/status` endpoint returns valid JSON

3. **Integration:**
   - Click "Run Analysis" on frontend
   - Check browser console for API errors
   - View backend logs for issues

---

## Troubleshooting

### GitHub Pages not updating
- Verify files are in correct folder
- Check Actions tab for workflow errors
- Clear browser cache (Ctrl+Shift+Delete)

### Backend API 404
- Verify backend is running
- Check API URL in frontend code
- Ensure CORS is enabled in flask_app.py

### CORS Errors
```
Access to XMLHttpRequest blocked by CORS policy
```
Solution: CORS already enabled in flask_app.py. If still issues:
```bash
pip install flask-cors
```

### Heroku app crashes
```bash
heroku logs --tail
```
Check for missing dependencies in requirements.txt

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Deploy backend to Heroku/PythonAnywhere/Railway
4. ✅ Update frontend API URL
5. ✅ Test full integration
6. ✅ Share your site!

---

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Heroku Deployment](https://devcenter.heroku.com/articles/deploying-python-apps-on-heroku)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
