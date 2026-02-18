from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    # App
    APP_NAME: str = "LightRAG Chatbot"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/lightrag"
    
    # LightRAG Mode
    LIGHTRAG_MODE: Literal["local", "runpod"] = "local"
    WORKING_DIR: str = "./lightrag_cache"
    
    # LLM Provider (openrouter, gemini, openai, ollama, vnpay)
    LLM_PROVIDER: Literal["openrouter", "gemini", "openai", "ollama", "vnpay"] = "openrouter"
    
    # OpenRouter (FREE models available!)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "google/gemma-3n-e4b-it:free"
    OPENROUTER_SITE_URL: str = ""
    OPENROUTER_SITE_NAME: str = ""

    # VNPay AI Gateway (Internal)
    VNPAY_API_KEY: str = ""
    VNPAY_BASE_URL: str = "https://genai.vnpay.vn/aigateway/llm_v4/v1"
    VNPAY_MODEL: str = "v_chat4"
    
    # Gemini (for local mode - FREE tier available!)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"  # or gemini-1.5-pro
    GEMINI_EMBEDDING_MODEL: str = "models/text-embedding-004"
    
    # OpenAI (optional - if you have quota)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # RunPod (for indexing mode)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:32b"
    EMBEDDING_MODEL: str = "bge-m3"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()

