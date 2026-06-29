# 📁 Project Structure - Aegis AI

```
depi_project/
│
├── 📂 frontend/                    # Frontend (HTML/CSS/JS)
│   ├── index.html                  # Main UI page
│   ├── api.js                      # API integration helper
│   └── config.js                   # Frontend configuration
│
├── 📂 backend/                     # Backend (FastAPI/Python)
│   ├── app/
│   │   ├── api/                    # API endpoints
│   │   │   ├── scenarios.py        # Scenario generation & classification
│   │   │   ├── organizations.py    # Organization stats & departments
│   │   │   ├── users.py            # User management
│   │   │   ├── leaderboard.py      # Leaderboard endpoints
│   │   │   └── __init__.py
│   │   ├── models/                 # Pydantic data models
│   │   │   ├── scenario.py         # Scenario models
│   │   │   ├── organization.py     # Organization models
│   │   │   ├── user.py             # User models
│   │   │   └── __init__.py
│   │   ├── services/               # Business logic
│   │   │   ├── ai_service.py       # Claude AI integration
│   │   │   └── __init__.py
│   │   ├── core/                   # Core configuration
│   │   │   ├── config.py           # Settings & env vars
│   │   │   ├── supabase.py         # Supabase client
│   │   │   └── __init__.py
│   │   ├── main.py                 # FastAPI app entry
│   │   └── __init__.py
│   ├── requirements.txt            # Python dependencies
│   ├── run.py                      # Run script
│   └── .env.example                # Environment variables template
│
├── 📂 database/                    # Database schemas
│   └── schema.sql                  # Supabase PostgreSQL schema
│
├── 📂 docs/                        # Documentation
│   ├── SETUP.md                    # Installation guide
│   ├── API.md                      # API documentation
│   └── DEPLOYMENT.md               # Deployment guide
│
├── README.md                       # Main project documentation
├── START.md                        # Quick start guide (Arabic/English)
├── PROJECT_STRUCTURE.md            # This file
└── .gitignore                      # Git ignore rules
```

## 🔍 File Descriptions

### Frontend
- **index.html**: Complete single-page application with all UI
- **api.js**: Helper functions for backend communication
- **config.js**: Configuration constants and settings

### Backend API Endpoints
- **scenarios.py**: Generate AI scenarios, classify user responses
- **organizations.py**: Department stats, risk assessment
- **users.py**: User CRUD operations
- **leaderboard.py**: Points, rankings, badges

### Backend Models
- **scenario.py**: Request/response models for scenarios
- **organization.py**: Department and org statistics models
- **user.py**: User and leaderboard entry models

### Backend Services
- **ai_service.py**: Claude API integration for scenario generation

### Backend Core
- **config.py**: Environment configuration using pydantic-settings
- **supabase.py**: Supabase database client initialization

### Database
- **schema.sql**: Complete PostgreSQL schema with:
  - users table
  - departments table
  - scenarios table
  - quiz_results table
  - Indexes and RLS policies

## 🎯 Key Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML/CSS/JS | User interface |
| Backend | FastAPI | REST API server |
| Database | Supabase (PostgreSQL) | Data storage |
| AI | Anthropic Claude | Scenario generation |
| Auth | Supabase Auth | User authentication |

## 📦 Dependencies

### Backend (requirements.txt)
- fastapi - Web framework
- uvicorn - ASGI server
- pydantic - Data validation
- supabase - Database client
- anthropic - Claude AI client
- python-dotenv - Environment variables

### Frontend
- No dependencies! Pure HTML/CSS/JavaScript
- Modern browsers only (ES6+)

## 🔄 Data Flow

```
User → Frontend (index.html)
  ↓
  → api.js (fetch request)
      ↓
      → Backend API (FastAPI)
          ↓
          → Service Layer (ai_service.py)
              ↓
              → Claude API / Supabase
                  ↓
                  ← Response
              ↓
          ← JSON Response
      ↓
  ← Display to User
```

## 🏗️ Architecture

**Frontend**: Single-page application (SPA)
- Vanilla JavaScript (no framework)
- State management in global `state` object
- Renders different views based on `state.view`

**Backend**: RESTful API
- FastAPI with automatic OpenAPI docs
- Modular router-based architecture
- Async/await for all endpoints

**Database**: Relational (PostgreSQL via Supabase)
- Normalized schema
- Row-level security (RLS)
- Automatic timestamps

**AI**: Anthropic Claude API
- System prompt engineering
- JSON response parsing
- Error handling & retries

## 🔐 Security

- Environment variables for secrets
- CORS configuration
- Supabase RLS policies
- Input validation with Pydantic
- SQL injection protection (ORM)

## 📈 Scalability

Current setup handles:
- **Users**: Thousands (Supabase free tier)
- **Requests**: ~500/hour (FastAPI)
- **AI Calls**: Limited by Anthropic API quota

For production scale:
- Add caching (Redis)
- Load balancer
- Horizontal scaling
- CDN for frontend
