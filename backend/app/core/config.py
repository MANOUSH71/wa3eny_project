from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    SECRET_KEY: str = "dev-secret-change-in-production"
    ENVIRONMENT: str = "development"
    
    # JWT Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()