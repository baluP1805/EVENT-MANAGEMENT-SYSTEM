# Vercel Deployment Guide

This guide covers deploying the College Event Management System frontend to Vercel and configuring it to work with your Supabase backend.

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub/GitLab/Bitbucket repository with your project
- Backend deployed and running (see Backend Deployment below)

### Step 1: Prepare Frontend for Vercel

The frontend is a static HTML/CSS/JavaScript application in the `frontend/` directory.

1. Ensure `frontend/js/config.js` is properly configured with runtime API URL support:
   ```javascript
   // config.js - runtime configuration
   window.API_BASE_URL = window.API_BASE_URL || 'http://localhost:5000';
   ```

2. All frontend pages should include `config.js` in their `<head>`:
   ```html
   <script src="../js/config.js"></script>
   ```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
npm install -g vercel
cd frontend
vercel --prod
```

#### Option B: Using Vercel Dashboard
1. Go to https://vercel.com/new
2. Import your Git repository
3. Set build settings:
   - **Framework Preset**: Other (static files)
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: `.` (current directory)

4. Environment Variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend URL (e.g., `https://your-backend.com`)

### Step 3: Configure API Base URL

After deployment, set the backend API URL by either:

#### Method 1: Environment Variable (Recommended)
Set `NEXT_PUBLIC_API_BASE_URL` in Vercel dashboard:
- Go to Project Settings → Environment Variables
- Add: `NEXT_PUBLIC_API_BASE_URL = https://your-backend-domain.com`

#### Method 2: Runtime Configuration
Modify `frontend/js/config.js` before deployment:
```javascript
window.API_BASE_URL = 'https://your-backend-domain.com';
```

#### Method 3: Query Parameter (Client-side)
The frontend checks for `?api=` query parameter:
```
https://your-app.vercel.app/?api=https://your-backend.com
```

## Backend Deployment

### Prerequisites
- Supabase project set up with tables created
- Backend environment variables configured
- Python 3.13+ and pip installed

### Step 1: Prepare Backend

1. Ensure `.env` file in `backend/` contains:
   ```
   USE_SUPABASE=true
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_anon_key
   SECRET_KEY=your-secret-key-change-in-production
   JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
   ```

2. Run migrations to copy data to Supabase:
   ```bash
   cd backend
   python migrate_to_supabase.py
   ```

### Step 2: Choose Hosting Platform

#### Option A: Heroku (Simple, Free tier available)
1. Create account at https://heroku.com
2. Install Heroku CLI and login
3. Create `Procfile` in project root:
   ```
   web: cd backend && gunicorn app:app
   ```

4. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set USE_SUPABASE=true
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_KEY=your_key
   heroku config:set SECRET_KEY=your_secret
   git push heroku main
   ```

#### Option B: Railway (Modern alternative to Heroku)
1. Create account at https://railway.app
2. Connect GitHub repository
3. Add environment variables in Railway dashboard
4. Deploy with one click

#### Option C: AWS/Google Cloud/Azure (Advanced)
- Use their app services (App Engine, Elastic Beanstalk, Container Apps)
- Deploy as Docker container or Python WSGI app
- Configure environment variables in their dashboards

#### Option D: Self-hosted VPS
- Deploy on your own server using gunicorn + nginx
- Set up SSL/TLS certificates (Let's Encrypt)
- Configure firewall and security

### Step 3: Update Frontend API URL

After backend is deployed, update the frontend's API base URL:

1. In Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Update/Add `NEXT_PUBLIC_API_BASE_URL` with your backend domain

2. Or update in code and redeploy:
   - Modify `frontend/js/config.js`
   - Push changes to trigger Vercel redeploy

## Testing Deployment

### Frontend Test
1. Open your Vercel URL in browser
2. Go to Login page → check browser console for API calls
3. Verify no CORS errors (should connect to backend)

### Backend Test
```bash
curl https://your-backend.com/  # Should return 404 or Flask welcome
curl -X GET https://your-backend.com/api/events  # Should return events
```

### Migration Status
Verify data in Supabase:
1. Open Supabase dashboard
2. Go to SQL Editor
3. Run:
   ```sql
   SELECT COUNT(*) FROM students;
   SELECT COUNT(*) FROM events;
   SELECT COUNT(*) FROM attendance;
   ```

## Troubleshooting

### CORS Errors
If frontend gets CORS errors when calling backend:
1. Check `backend/config.py` for `CORS` configuration
2. Update allowed origins if needed
3. Ensure backend includes `Access-Control-Allow-Origin` headers

### API URL Not Resolving
- Verify `frontend/js/config.js` is loaded (check Network tab in DevTools)
- Confirm backend URL is accessible and returns data
- Check for typos in environment variables

### Database Connection Issues
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in backend environment
- Test Supabase connectivity:
  ```bash
  python -c "from supabase_client import get_supabase_client; c = get_supabase_client(); print(c.rest_url)"
  ```

### Deployment Failed
- Check logs in your hosting platform dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies
- Test locally before deploying

## Security Checklist

- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY` to random strings
- [ ] Add Supabase anon key (not service_role key) to backend
- [ ] Enable HTTPS on backend domain
- [ ] Set `MAIL_USERNAME` and `MAIL_PASSWORD` for email notifications
- [ ] Configure rate limiting and session timeouts
- [ ] Review CORS allowed origins
- [ ] Keep dependencies updated (`pip list --outdated`)
- [ ] Monitor logs for suspicious activity

## Scaling & Performance

### Frontend (Vercel)
- Automatically scaled via CDN
- Consider caching static assets
- Monitor analytics for slow pages

### Backend
- Use connection pooling for Supabase
- Add caching for frequently accessed data
- Monitor response times and database queries
- Consider horizontal scaling if traffic increases
- Use load balancer if running multiple backend instances

## Next Steps

1. Deploy backend to your chosen platform
2. Configure Supabase credentials in backend environment
3. Test backend connectivity from frontend
4. Deploy frontend to Vercel
5. Test end-to-end workflow (login → events → scan)
6. Monitor logs and performance

For support, refer to:
- Vercel docs: https://vercel.com/docs
- Supabase docs: https://supabase.com/docs
- Flask docs: https://flask.palletsprojects.com
