# Aegis AI - Cybersecurity Awareness Platform

AI-powered platform for phishing detection training using **FastAPI + Supabase + Claude AI**

## 🏗️ Project Structure

```
depi_project/
├── frontend/          # HTML/CSS/JavaScript UI
│   └── index.html
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── models/    # Pydantic models
│   │   ├── services/  # Business logic
│   │   ├── core/      # Config & DB
│   │   └── main.py    # FastAPI app
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## 🚀 Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: FastAPI (Python 3.10+)
- **Database**: Supabase (PostgreSQL)
- **AI**: Anthropic Claude API
- **Auth**: Supabase Auth

## ⚡ Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
# Open index.html in browser
# Or use Python server:
python -m http.server 8080
```

### 3. Get API Keys

**Anthropic Claude API**:
1. Go to https://console.anthropic.com/
2. Create account → Get API key
3. Add to `.env`: `ANTHROPIC_API_KEY=your_key_here`

**Supabase**:
1. Go to https://supabase.com/
2. Create new project
3. Get URL & anon key from Settings
4. Add to `.env`:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

## 📊 Database Schema (Supabase)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    points INTEGER DEFAULT 0,
    badge TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Departments table
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    attempts INTEGER DEFAULT 0,
    score_sum INTEGER DEFAULT 0,
    correct INTEGER DEFAULT 0,
    risk_level INTEGER,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Scenarios table
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    department_key TEXT,
    channel TEXT,
    is_phishing BOOLEAN,
    user_classification BOOLEAN,
    score INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🎯 Features

- ✅ AI-generated phishing scenarios (Email, WhatsApp, Login Pages)
- ✅ Interactive simulation & instant feedback
- ✅ Organization dashboard & risk assessment
- ✅ Department-specific training (Accounting, HR, IT, Marketing, Sales)
- ✅ Individual training modes (Banking, Shopping, Social Media)
- ✅ Senior citizen awareness program
- ✅ Leaderboard & gamification (points & badges)
- ✅ Real-time risk scoring

## 📡 API Endpoints

```
GET  /                      - API info
GET  /health                - Health check
POST /api/scenarios/generate - Generate AI scenario
POST /api/scenarios/classify - Submit classification
GET  /api/organizations/stats - Get org stats
POST /api/organizations/departments/update - Update dept
GET  /api/leaderboard       - Get top users
POST /api/users             - Create user
GET  /api/users/{id}        - Get user info
```

Full docs at: `http://localhost:8000/docs`

## 🔧 Development

```bash
# Backend (FastAPI)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend (any server)
cd frontend
python -m http.server 8080
```

## 📝 Environment Variables

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
ANTHROPIC_API_KEY=your_anthropic_api_key
SECRET_KEY=your-secret-key-for-jwt
ENVIRONMENT=development
```

## 🎓 Graduation Project

**Aegis AI** - AI-powered cybersecurity awareness platform
Built with FastAPI, Supabase, and Claude AI

---

**Made with ❤️ for cybersecurity awareness**
