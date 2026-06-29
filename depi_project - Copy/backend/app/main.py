from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import scenarios, organizations, users, leaderboard

app = FastAPI(
    title="Aegis AI API",
    description="Cybersecurity Awareness Training Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenarios.router, prefix="/api/scenarios", tags=["Scenarios"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["Organizations"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["Leaderboard"])

@app.get("/")
async def root():
    return {"message": "Aegis AI API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
