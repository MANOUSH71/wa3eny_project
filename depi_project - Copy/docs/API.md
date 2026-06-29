# API Documentation - Aegis AI

Base URL: `http://localhost:8000/api`

## Authentication
Currently uses Supabase anonymous access. Auth can be added later.

---

## Scenarios

### Generate Scenario
Generate AI-powered phishing training scenario

```http
POST /scenarios/generate
Content-Type: application/json

{
  "department": "accounting",  // or null
  "sector": "banking",          // or null
  "difficulty": "medium"        // easy|medium|hard
}
```

**Response:**
```json
{
  "channel": "email",
  "sender_name": "Finance Department",
  "sender_handle": "finance@company-mail.com",
  "title": "Urgent: Wire Transfer Required",
  "message": "Please process this wire transfer immediately...",
  "is_phishing": true,
  "red_flags": [
    "Urgent request creating psychological pressure",
    "Email domain does not match official domain"
  ],
  "correct_action": "Verify with finance department directly",
  "explanation": "This is a typical phishing attempt..."
}
```

### Classify Scenario
Submit user's classification and get score

```http
POST /scenarios/classify
Content-Type: application/json

{
  "scenario_id": "uuid-here",
  "user_classification": true,  // true=phishing, false=safe
  "selected_flags": [
    "Urgent request creating pressure",
    "Strange link"
  ]
}
```

**Response:**
```json
{
  "correct_classification": true,
  "score": 85,
  "feedback": "Good catch! You identified 2/3 red flags.",
  "flag_analysis": {
    "correct": 2,
    "wrong": 0,
    "missed": 1,
    "total": 3
  }
}
```

---

## Organizations

### Get Organization Stats
Get overall organization statistics

```http
GET /organizations/stats
```

**Response:**
```json
{
  "total_attempts": 120,
  "total_departments": 5,
  "average_score": 72.5,
  "high_risk_departments": 2,
  "last_updated": "2026-06-28T01:00:00Z"
}
```

### Update Department
Update department statistics after training

```http
POST /organizations/departments/update
Content-Type: application/json

{
  "department_key": "accounting",
  "score": 85,
  "correct": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Department stats updated"
}
```

### Get All Departments
Get statistics for all departments

```http
GET /organizations/departments
```

**Response:**
```json
[
  {
    "key": "accounting",
    "name": "Accounting",
    "icon": "💰",
    "description": "Fake invoices and urgent wire-transfer requests",
    "attempts": 25,
    "score_sum": 1850,
    "correct": 18,
    "risk_level": 26
  }
]
```

---

## Users

### Create User
Register a new user

```http
POST /users/
Content-Type: application/json

{
  "name": "Ahmed Ali",
  "email": "ahmed@example.com",
  "points": 0
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Ahmed Ali",
  "email": "ahmed@example.com",
  "points": 0,
  "badge": null,
  "created_at": "2026-06-28T01:00:00Z"
}
```

### Get User
Get user information by ID

```http
GET /users/{user_id}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Ahmed Ali",
  "points": 150,
  "badge": "Silver 🥈"
}
```

### Update User Points
Update user's points

```http
PUT /users/{user_id}/points?points=200
```

**Response:**
```json
{
  "success": true,
  "points": 200
}
```

---

## Leaderboard

### Get Leaderboard
Get top users by points

```http
GET /leaderboard/?limit=10&current_user_id=uuid
```

**Response:**
```json
[
  {
    "rank": 1,
    "name": "Mona Abdallah",
    "points": 260,
    "badge": "Silver 🥈",
    "is_current_user": false
  },
  {
    "rank": 2,
    "name": "Youssef El-Sherif",
    "points": 140,
    "badge": "Bronze 🥉",
    "is_current_user": true
  }
]
```

---

## Health & Status

### Root
API information

```http
GET /
```

**Response:**
```json
{
  "message": "Aegis AI API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Health Check
Check API health

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI with:
- Try endpoints directly
- View request/response schemas
- Test authentication
- Export API spec
