# 🚀 Quick Start - Aegis AI

## ⚡ السريع البدء

### 1️⃣ تشغيل Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# أضف API keys في ملف .env
python run.py
```

✅ Backend: `http://localhost:8000`
📚 API Docs: `http://localhost:8000/docs`

### 2️⃣ تشغيل Frontend

```bash
cd frontend
python -m http.server 8080
```

✅ Frontend: `http://localhost:8080`

---

## 🔑 API Keys المطلوبة

### Anthropic Claude API
1. https://console.anthropic.com/
2. Create account → API Keys → Create
3. نسخ المفتاح: `sk-ant-...`

### Supabase
1. https://supabase.com/
2. New Project
3. Settings → API
4. نسخ URL و anon key

### ملف .env

```env
ANTHROPIC_API_KEY=sk-ant-xxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx
SECRET_KEY=any-random-string-here
```

---

## 🗄️ Database Setup

1. افتح Supabase Dashboard
2. SQL Editor
3. انسخ محتوى `database/schema.sql`
4. Run

---

## ✅ اختبار

### Backend
```
http://localhost:8000/health
→ {"status": "healthy"}
```

### Frontend
1. افتح `http://localhost:8080`
2. Start as Organization
3. Select department
4. Generate Scenario

---

## 📖 التوثيق الكامل

- **Setup**: `docs/SETUP.md`
- **API**: `docs/API.md`
- **Deployment**: `docs/DEPLOYMENT.md`

---

## 🎯 المميزات

✅ AI-generated phishing scenarios
✅ Organization dashboard
✅ Department training
✅ Individual mode
✅ Senior citizen mode
✅ Leaderboard & gamification

---

## 🆘 مشاكل شائعة

**Backend لا يعمل؟**
- تأكد Python 3.10+
- تفعيل venv
- API keys صحيحة

**Frontend لا يتصل؟**
- Backend يعمل؟
- Port 8000 فاضي؟
- Check browser console

**Database أخطاء؟**
- Supabase project active
- schema.sql تم تشغيله
- API keys صحيحة

---

**Made with ❤️ - Aegis AI Graduation Project**
