# Deployment Guide - Aegis AI

## Production Deployment Options

### Option 1: Railway (Recommended for Backend)

**Why Railway?**
- Free tier available
- Automatic deployments from GitHub
- Built-in PostgreSQL
- Simple Python deployment

**Steps:**

1. **Prepare Repository**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-repo-url
git push -u origin main
```

2. **Deploy on Railway**
- Visit https://railway.app/
- Connect GitHub account
- Click "New Project" → "Deploy from GitHub"
- Select your repository
- Railway auto-detects Python
- Add environment variables in dashboard:
  - `ANTHROPIC_API_KEY`
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `SECRET_KEY`
  - `ENVIRONMENT=production`

3. **Configure Build**
Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Option 2: Render

**Steps:**

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: aegis-ai-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
```

2. Deploy:
- Visit https://render.com/
- Connect GitHub
- Select repository
- Render auto-deploys

### Option 3: Vercel (Frontend) + Railway (Backend)

**Frontend on Vercel:**
```bash
cd frontend
vercel --prod
```

**Backend on Railway:**
(See Railway steps above)

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

```bash
npm install -g vercel
cd frontend
vercel --prod
```

Update API URL in `api.js`:
```javascript
const API_BASE_URL = 'https://your-backend.railway.app/api';
```

### Option 2: Netlify

```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

### Option 3: GitHub Pages

1. Create `frontend/.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend
```

---

## Database (Supabase)

**Already cloud-hosted!** No deployment needed.

Just update URLs in production environment variables.

---

## Production Checklist

### Security
- [ ] Change `SECRET_KEY` to random string
- [ ] Enable CORS only for your domain
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Set `ENVIRONMENT=production`

### Backend
- [ ] Update CORS allowed origins
- [ ] Add logging (Sentry/LogRocket)
- [ ] Setup monitoring
- [ ] Configure backup

### Frontend
- [ ] Update API_BASE_URL to production
- [ ] Minify CSS/JS
- [ ] Add Google Analytics (optional)
- [ ] Test on mobile devices

### Database
- [ ] Enable RLS policies
- [ ] Setup backups
- [ ] Monitor usage
- [ ] Setup alerting

---

## Environment Variables (Production)

```env
# Backend (.env)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_production_key
ANTHROPIC_API_KEY=sk-ant-xxx
SECRET_KEY=super-secret-random-key-min-32-chars
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## Monitoring & Logs

### Backend Logs (Railway)
```bash
railway logs
```

### Frontend (Vercel)
- Dashboard → Your Project → Logs

### Database (Supabase)
- Dashboard → Logs → API/Database

---

## Custom Domain

### Backend (Railway)
1. Railway Dashboard → Settings → Domains
2. Add custom domain: `api.yourdomain.com`
3. Add CNAME record in DNS

### Frontend (Vercel)
1. Vercel Dashboard → Settings → Domains
2. Add domain: `yourdomain.com`
3. Follow DNS instructions

---

## Cost Estimate (Free Tier)

- **Railway**: Free tier (512MB RAM, 500 hours/month)
- **Vercel**: Free tier (100GB bandwidth)
- **Supabase**: Free tier (500MB database, 2GB storage)
- **Anthropic API**: Pay per use (~$3 per 1M tokens)

**Total**: ~$0-10/month depending on usage

---

## Scaling Considerations

When you outgrow free tier:

1. **Backend**: Railway Pro ($5/month) or AWS/GCP
2. **Database**: Supabase Pro ($25/month) or self-hosted
3. **CDN**: Cloudflare (free) for caching
4. **Monitoring**: Sentry (free tier) for error tracking

---

## Rollback Strategy

### Railway
- Dashboard → Deployments → Redeploy previous version

### Vercel
- Dashboard → Deployments → Promote previous

### Database
- Supabase → Database → Point-in-time recovery

---

## Support & Maintenance

- Monitor error logs daily
- Check API usage weekly
- Backup database monthly
- Update dependencies quarterly
- Review security annually
