from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    SECRET_KEY: str = "dev-secret-change-in-production"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
