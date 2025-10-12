from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

def env(key: str, default: str = None):
    """Environment variable helper"""
    return os.getenv(key, default)


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = env("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = env("PROJECT_NAME", "Blind Test Backend")
    
    # Database Settings
    DATABASE_URL: str = env("DATABASE_URL", "postgresql://user:password@localhost/blind_test_db")
    
    # Security Settings
    SECRET_KEY: str = env("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = env("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(env("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(env("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Email Settings
    MAIL_USERNAME: Optional[str] = env("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = env("MAIL_PASSWORD")
    MAIL_FROM: Optional[str] = env("MAIL_FROM")
    MAIL_PORT: int = int(env("MAIL_PORT", "587"))
    MAIL_SERVER: Optional[str] = env("MAIL_SERVER")
    MAIL_TLS: bool = env("MAIL_TLS", "true").lower() == "true"
    MAIL_SSL: bool = env("MAIL_SSL", "false").lower() == "true"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: str = env("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
    
    # Debug Mode
    DEBUG: bool = env("DEBUG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
