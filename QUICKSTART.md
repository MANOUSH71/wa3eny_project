# ⚡ Quick Start Guide - Aegis AI

Get up and running in **5 minutes**!

## Prerequisites

- Python 3.10+
- Web browser
- Internet connection

## 🚀 Steps

### 1. Get API Keys (2 minutes)

**Anthropic Claude:**
```
1. Go to: https://console.anthropic.com/
2. Sign up → API Keys → Create Key
3. Copy key (starts with sk-ant-)
```

**Supabase:**
```
1. Go to: https://supabase.com/
2. New Project → Wait 2 minutes
3. Settings → API → Copy URL & Key
```

### 2. Setup Backend (1 minute)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3. Configure (30 seconds)

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key-here
```

### 4. Setup Database (1 minute)

```
1. Open Supabase Dashboard
2. SQL Editor → New Query
3. Copy content from database/schema.sql
4. Run
```

### 5. Run (30 seconds)

**Backend:**
```bash
cd backend
python run.py
```
✅ http://localhost:8000

**Frontend:**
```bash
cd frontend
python -m http.server 8080
```
✅ http://localhost:8080

## 🎉 Done!

Visit http://localhost:8080 and start training!

## 🆘 Problems?

**Backend won't start?**
- Check Python version: `python --version`
- Activate venv first
- Check .env file has all keys

**Frontend can't connect?**
- Backend running?
- Try different port: `python -m http.server 8081`

**AI not working?**
- Check Anthropic API key is correct
- Check you have API credits

## 📚 Next Steps

- Read full docs: `docs/SETUP.md`
- Check API: http://localhost:8000/docs
- Try all features!

---

**Total Time: ~5 minutes** ⏱️
