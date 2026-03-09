# Vercel Deployment Guide

## Files added for Vercel

| File | Purpose |
|---|---|
| `vercel.json` | Routes `/api/*` → Flask serverless function, everything else → static frontend |
| `api/index.py` | Vercel entrypoint — imports `app` from `backend/app.py` |
| `requirements.txt` (root) | Python dependencies read by Vercel during build |

---

## Steps to deploy

### 1. Push to GitHub
Make sure all changes are committed and pushed to the `main` branch of `baluP1805/EVENT-MANAGEMENT-SYSTEM`.

### 2. Import project in Vercel
1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Click **Import Git Repository** → select `baluP1805/EVENT-MANAGEMENT-SYSTEM`
3. **Framework Preset**: leave as **Other**
4. **Root Directory**: leave as `.` (repo root)
5. Do NOT set a custom build command — `vercel.json` handles it

### 3. Set Environment Variables
In **Settings → Environment Variables** add every variable below:

| Variable | Value |
|---|---|
| `SECRET_KEY` | `college-ems-secret-key-2026` |
| `JWT_SECRET_KEY` | `college-ems-jwt-secret-2026` |
| `USE_SUPABASE` | `true` |
| `SUPABASE_URL` | `https://clcgfbvadsdaeczwtnge.supabase.co` |
| `SUPABASE_KEY` | *(your supabase anon key)* |
| `ADMIN_EMAIL` | `admin@college.edu` |
| `ADMIN_PASSWORD` | `123@Admin` |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USERNAME` | `pbalu1805@gmail.com` |
| `MAIL_PASSWORD` | `vfmd dsdr mcvl liya` |
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |

> **Important**: Never commit `.env` to GitHub. Vercel reads these from the dashboard.

### 4. Deploy
Click **Deploy**. The build should complete in ~60 seconds.

### 5. Update frontend API URL
After the first deployment, copy your Vercel project URL (e.g. `https://event-management-system.vercel.app`).

Open `frontend/js/config.js` and set:
```js
const API_BASE_URL = 'https://your-project.vercel.app/api';
```
Then redeploy.

---

## How the routing works

```
GET /                       → frontend/index.html
GET /pages/events.html      → frontend/pages/events.html
GET /css/style.css          → frontend/css/style.css
GET /api/auth/login         → api/index.py  (Flask)
GET /api/admin/dashboard    → api/index.py  (Flask)
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `No flask entrypoint found` | Make sure `api/index.py` exists and `vercel.json` points `src` to `api/index.py` |
| `ModuleNotFoundError: backend` | `api/index.py` adds `backend/` to `sys.path` — check file exists |
| 500 on `/api/*` | Check Vercel function logs; likely a missing env variable |
| CORS errors in browser | Vercel URL must be added to allowed origins if you restrict CORS |
