# Render Deployment Guide

## Pre-Deployment Checklist

- [x] Frontend Dockerfile created (`frontend/Dockerfile`)
- [x] Nginx configuration created (`frontend/nginx.conf`)
- [x] Frontend API config created (`frontend/src/config.ts`)
- [x] Backend CORS updated for Render domains
- [x] Database configuration updated (PostgreSQL support)
- [x] Docker entrypoint updated to run migrations
- [x] Health check endpoint available (`/health`)
- [x] Infrastructure-as-code config created (`render.yaml`)

## Deployment Steps

### 1. Push All Changes to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 3. Deploy PostgreSQL Database

1. From Render Dashboard: **New +** → **PostgreSQL**
2. Configure:
   - **Name**: `schemeassist-db`
   - **Database**: `schemeassist`
   - **Region**: Choose closest to you (default: Oregon)
   - **Plan**: **Free** (no credit card)
3. Click **Create Database**
4. Wait ~2 minutes for provisioning
5. **Save these values** from "Info" tab:
   - **Internal Database URL** (for backend connection)
   - **External Database URL** (for local testing)

### 4. Deploy Backend Service

1. **New +** → **Web Service**
2. Connect repository: `civoranexus/aid105-Astroking2004`
3. Configure:
   - **Name**: `schemeassist-backend`
   - **Region**: Same as database (Oregon)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `src/backend/Dockerfile`
   - **Docker Context**: `.`
   - **Plan**: Free (512 MB RAM)

4. Add Environment Variables (click "Advanced"):
   ```
   DATABASE_URL = [Paste Internal Database URL from Step 3]
   PYTHONUNBUFFERED = 1
   ALLOW_ALL_ORIGINS = false
   ```

5. Click **Create Web Service**
6. Wait 5-10 minutes for first build
7. **Save Backend URL**: `https://schemeassist-backend.onrender.com`

### 5. Deploy Frontend Service

1. **New +** → **Web Service**
2. Connect same repository
3. Configure:
   - **Name**: `schemeassist-frontend`
   - **Region**: Same as backend (Oregon)
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `frontend/Dockerfile`
   - **Docker Context**: `frontend`
   - **Plan**: Free

4. Add Environment Variables:
   ```
   VITE_API_URL = https://schemeassist-backend.onrender.com
   NODE_ENV = production
   ```

5. Update `frontend/nginx.conf` with your backend URL if different
6. Commit and push changes
7. Click **Create Web Service**
8. Wait 3-5 minutes for build

## Your Live URLs

- **Frontend**: `https://schemeassist-frontend.onrender.com`
- **Backend API**: `https://schemeassist-backend.onrender.com`
- **API Docs**: `https://schemeassist-backend.onrender.com/docs`
- **Health Check**: `https://schemeassist-backend.onrender.com/health`

## Post-Deployment Tasks

### Run Initial Data Import

1. Go to Backend Service → **Shell** tab
2. Run:
   ```bash
   cd /app
   python import_schemes.py
   ```

### Database Migrations

Migrations run automatically via `docker-entrypoint.sh`, but to verify:

1. Backend Service → **Shell** → Run:
   ```bash
   cd /app
   python -m alembic current
   ```

## Automatic Deployments

Every time you push to `main`, Render automatically:
1. Detects changes
2. Rebuilds and redeploys services
3. Takes ~5-10 minutes

To disable: Service Settings → Build & Deploy → Auto-Deploy: **OFF**

## Troubleshooting

### Backend won't start
- Check logs in Dashboard
- Verify DATABASE_URL starts with `postgresql://` (not `postgres://`)
- Ensure migrations complete: `alembic current`

### Frontend can't reach backend
- Verify CORS origins in backend include frontend URL
- Check nginx.conf has correct backend URL
- Ensure backend service is running

### 502 Bad Gateway
- Usually means backend crashed (check logs)
- Or free tier service is sleeping (30s wake-up)
- Or wrong port in Dockerfile (ensure 8000 for backend)

### Database Connection Error
- Use INTERNAL Database URL for backend (not external)
- Check DATABASE_URL format: `postgresql://user:pass@host:5432/dbname`

## Cost Breakdown

**Free Tier:**
- ✅ 1 PostgreSQL DB: 1GB storage, 97 hrs/month
- ✅ 2 Web Services: 750 hrs/month each
- ⚠️ Services sleep after 15 min inactivity
- ⚠️ Deleted after 90 days of inactivity

**To prevent sleeping (paid):**
- Starter: $7/month per service
- Pro: $25/month per service (auto-scaling)

## Optional Enhancements

### Custom Domain
Service Settings → Custom Domains → Add your domain

### Environment-based Configuration
Use `render.yaml` for infrastructure-as-code:
```bash
render deploy
```

### Health Checks
Already configured at `/health` endpoint
Render monitors: Dashboard → Service → Health
