# Render Deployment Guide

## What Gets Configured Automatically on Render

When you upload this project to Render, here's what happens with the configuration:

### 1. **Start Command**
```bash
gunicorn space_weather_dashboard.wsgi
```
- Starts the Django application using Gunicorn as the production WSGI server
- Renders manages the process automatically

### 2. **Build Process**
- Installs dependencies from `requirements.txt`
- Collects static files
- Runs migrations (if configured)

### 3. **Environment Variables** (Set in Render Dashboard)
You need to set these in Render's dashboard:

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Generate new secure key | Use Django command: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | Never `True` in production |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` | Your Render domain |
| `NASA_API_KEY` | Your API key | Get from https://api.nasa.gov |

## Step-by-Step Deployment

### 1. Generate a new SECRET_KEY
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```
Copy the output.

### 2. Connect GitHub to Render
- Go to https://dashboard.render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository and branch

### 3. Configure the Service
- **Name**: `space-weather-dashboard` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn space_weather_dashboard.wsgi`

### 4. Set Environment Variables
- Click "Environment"
- Add the following:
  - `SECRET_KEY`: Paste the generated key
  - `DEBUG`: `False`
  - `ALLOWED_HOSTS`: Your Render domain (e.g., `space-weather-dashboard.onrender.com`)
  - `NASA_API_KEY`: Your NASA API key

### 5. Deploy
- Click "Create Web Service"
- Render will automatically deploy and run your app

## Important Notes

### Static Files
- WhiteNoise middleware is configured to serve static files in production
- Static files are collected to `staticfiles/` directory
- No separate static file server needed

### Database
**Current**: SQLite (works on Render but not persistent)

**Recommended for Production**: PostgreSQL
```python
# In settings.py, use:
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
```

### Updates to Project Files
✅ `requirements.txt` - Added: gunicorn, python-dotenv, whitenoise
✅ `settings.py` - Updated for environment variables
✅ `render.yaml` - Render configuration file
✅ `.env.example` - Template for environment variables
✅ `.gitignore` - Updated with production files

## Testing Locally Before Deploying

```bash
# Create .env file from .env.example
cp .env.example .env

# Edit .env with test values
nano .env

# Install new dependencies
pip install -r requirements.txt

# Test with Gunicorn
gunicorn space_weather_dashboard.wsgi --bind 0.0.0.0:8000
```

Visit `http://localhost:8000` to verify it works.

## Troubleshooting

### 502 Bad Gateway Error
- Check Build Logs in Render dashboard
- Ensure all environment variables are set
- Check `SECRET_KEY` is valid

### Static files not loading
- Verify `STATIC_ROOT` is set correctly
- Run `collectstatic` command

### Database errors
- Ensure migrations ran in build command
- Check database configuration in environment variables

## Support
- Render Docs: https://docs.render.com
- Django Deployment: https://docs.djangoproject.com/en/5.1/howto/deployment/
