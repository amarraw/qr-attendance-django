# Render Deployment Guide

This guide walks you through deploying the QR Attendance system to Render.

## Prerequisites
- GitHub account with repository created for this project
- Render account (free at https://render.com)
- All changes committed to GitHub

## Step 1: Push to GitHub

From the project directory:

```powershell
git init
git add .
git commit -m "QR Attendance ready for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/qr-attendance-django.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and `qr-attendance-django` with your repo name.

## Step 2: Create Render Account & Connect GitHub

1. Go to https://render.com and sign up
2. Click "Connect GitHub" and authorize Render
3. Select the qr-attendance-django repository

## Step 3: Create Web Service on Render

1. From Render dashboard, click "New +" → "Web Service"
2. Select your `qr-attendance-django` repository
3. Configure:
   - **Name**: `qr-attendance`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn qr_attendance.wsgi
     ```
   - **Plan**: Free tier (auto-sleeps after 15 min inactivity)

## Step 4: Set Environment Variables

In Render dashboard for your service, go to "Environment" and add:

```
DEBUG=False
SECRET_KEY=<generate-random-key-below>
ALLOWED_HOSTS=<your-render-url>.onrender.com
```

### Generate SECRET_KEY

Run this Python command to generate a secure key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste as `SECRET_KEY` value in Render.

Your Render URL will be shown after you create the service (e.g., `https://qr-attendance-xxxxx.onrender.com`).

## Step 5: Deploy

Click "Create Web Service" and Render will:
1. Build the app (2-3 min)
2. Run migrations automatically
3. Collect static files
4. Deploy to production HTTPS URL

Your app will be live at: `https://<your-render-url>.onrender.com`

## Step 6: Verify Deployment

1. Visit your Render URL
2. Try student login/registration
3. Access admin panel at `/adminpanel/login/`
4. Test QR scanner (camera requires HTTPS)
5. Test PWA installability (should show "Install app" prompt)

## Troubleshooting

### Build Errors
- Check Render logs: Dashboard → Select service → "Logs"
- Common: Missing migrations or static files

### Database Errors
- Render auto-creates PostgreSQL, but migrations must run successfully
- Check logs for migration errors
- Can manually run: Render Shell → `python manage.py migrate`

### Camera Not Working on Mobile
- Ensure you're on the Render HTTPS URL (not HTTP)
- Camera requires HTTPS for security reasons
- File upload fallback should always work

### Cold Starts
- Free tier sleeps after 15 min inactivity
- First request after sleep takes ~10s (normal)
- Paid plans have always-on option

## Scaling Up

To switch to paid plan:
1. Dashboard → Select service
2. Click "Settings" → Change plan
3. Select instance with more resources
4. Never sleeps, better performance

## Next Steps

- Replace placeholder PWA icons (192x192, 512x512 PNG)
- Build native Android/iOS app with Capacitor
- Set up GitHub Actions for auto-deploy on push
- Monitor app usage in Render dashboard
