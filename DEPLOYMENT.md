# 🚀 Deployment Guide - Render.com

This guide will help you deploy your Flight Price Tracker to Render.com (free tier).

## Prerequisites

- GitHub account
- Render.com account (free)
- Your code pushed to GitHub

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Full-stack Flight Price Tracker with React + Flask"
git push origin main
```

## Step 2: Deploy Backend (Flask API)

### 2.1 Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your **Flight-Price-Tracker** repo

### 2.2 Configure Backend Service

**Settings:**
- **Name**: `flight-tracker-api` (or your choice)
- **Environment**: `Docker`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Dockerfile Path**: `./Dockerfile`

**Environment Variables:**
- No additional variables needed!

**Instance Type:**
- **Free** (enough for this app)

### 2.3 Deploy

- Click **"Create Web Service"**
- Wait 5-10 minutes for build (Docker + Chrome installation)
- Note your backend URL: `https://flight-tracker-api.onrender.com`

## Step 3: Deploy Frontend (React)

### 3.1 Create Static Site on Render

1. Go back to Render Dashboard
2. Click **"New +"** → **"Static Site"**
3. Connect same GitHub repository
4. Select your **Flight-Price-Tracker** repo

### 3.2 Configure Frontend Service

**Settings:**
- **Name**: `flight-tracker-frontend` (or your choice)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Build Command**:
  ```
  cd frontend && npm install && npm run build
  ```
- **Publish Directory**:
  ```
  frontend/build
  ```

**Environment Variables:**
- **Key**: `REACT_APP_API_URL`
- **Value**: `https://flight-tracker-api.onrender.com` (your backend URL from Step 2)

### 3.3 Deploy

- Click **"Create Static Site"**
- Wait 3-5 minutes for build
- Your app will be live at: `https://flight-tracker-frontend.onrender.com`

## Step 4: Test Your Deployment

1. Visit your frontend URL
2. Enter flight details:
   - Origin: YYZ
   - Destination: LAX
   - Date: Any future date
   - Adults: 1
3. Click **Search Flights**
4. Wait 15-20 seconds
5. See results! ✈️

## Troubleshooting

### Backend Issues

**Build fails:**
- Check Dockerfile syntax
- Ensure backend/requirements.txt exists
- Check Render build logs

**Scraper fails:**
- Chrome might not be installing correctly
- Check timeout settings (set to 120s in Dockerfile)
- Verify Kayak hasn't changed their HTML structure

### Frontend Issues

**Build fails:**
- Ensure frontend/package.json exists
- Check npm install logs
- Verify all dependencies are listed

**Can't connect to backend:**
- Verify `REACT_APP_API_URL` is set correctly
- Check backend is deployed and healthy
- Open browser console for error messages

**CORS errors:**
- Backend has flask-cors installed
- Check backend logs for CORS configuration

## Free Tier Limits

**Render Free Tier:**
- 750 hours/month per service
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds to wake up
- Total: You can run both services 24/7 for free!

## Updating Your App

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push origin main

# Render will automatically redeploy both services!
```

## Custom Domain (Optional)

1. In Render Dashboard, go to your Static Site
2. Click **"Settings"** → **"Custom Domains"**
3. Add your domain
4. Update DNS records as instructed
5. Done!

## Cost Optimization

**If you exceed free tier:**
- Upgrade to paid tier ($7/month per service)
- Or reduce usage
- Or add a "sleep schedule" to turn off during low-traffic hours

## Need Help?

- Check Render docs: https://render.com/docs
- Backend logs: Render Dashboard → flight-tracker-api → Logs
- Frontend logs: Render Dashboard → flight-tracker-frontend → Logs
- GitHub Issues: [Your repo issues page]

---

**Happy Deploying! 🎉**
