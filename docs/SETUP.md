# Setup Guide - Aegis AI

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Supabase account
- Anthropic API key

## Step-by-Step Installation

### 1. Clone/Download Project

```bash
cd depi_project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get API Keys

#### Anthropic Claude API
1. Visit: https://console.anthropic.com/
2. Sign up/Login
3. Go to API Keys
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)

#### Supabase
1. Visit: https://supabase.com/
2. Create account
3. Click "New Project"
4. Set project name, database password, region
5. Wait for project to be created (~2 minutes)
6. Go to Settings → API
7. Copy:
   - Project URL
   - anon/public key

### 4. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
SECRET_KEY=your-random-secret-key-here
ENVIRONMENT=development
```

### 5. Setup Database

1. Open Supabase Dashboard
2. Go to SQL Editor
3. Copy content from `database/schema.sql`
4. Paste and click "Run"
5. Verify tables created in Table Editor

### 6. Run Backend

```bash
cd backend
python run.py
```

Or:
```bash
uvicorn app.main:app --reload
```

Backend will run at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### 7. Run Frontend

Option 1 - Direct open:
```bash
cd frontend
# Open index.html in browser
```

Option 2 - Python server:
```bash
cd frontend
python -m http.server 8080
```

Frontend will run at: `http://localhost:8080`

## Testing

### Test Backend
```bash
# Open browser
http://localhost:8000/health
# Should return: {"status": "healthy"}

# Test API docs
http://localhost:8000/docs
```

### Test Frontend
1. Open `http://localhost:8080`
2. Click "Start as an Organization"
3. Select a department
4. Click "Generate New Scenario"
5. Should see AI-generated phishing scenario

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.10+)
- Check venv is activated
- Check `.env` file exists with correct keys
- Check no other service using port 8000

### Frontend can't connect to backend
- Check backend is running at `http://localhost:8000`
- Check CORS is enabled (already configured)
- Check browser console for errors
- Try different port: `python -m http.server 8080`

### Database errors
- Verify Supabase project is active
- Check URL and key in `.env`
- Run schema.sql again in Supabase SQL Editor
- Check RLS policies in Supabase dashboard

### AI generation fails
- Verify Anthropic API key is correct
- Check API key has credits
- Check internet connection
- View error in browser console or backend logs

## Next Steps

1. ✅ Setup complete
2. 🎯 Test all features (scenarios, classification, leaderboard)
3. 📊 Check organization dashboard
4. 🏆 Try individual mode
5. 👴 Test senior citizen quiz
6. 🚀 Deploy to production (see DEPLOYMENT.md)

## Need Help?

- Backend logs: Check terminal running backend
- Frontend errors: Open browser DevTools (F12) → Console
- Database: Check Supabase Dashboard → Logs
