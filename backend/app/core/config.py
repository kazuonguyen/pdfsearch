from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multimodal Search API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql://user:password@db:5500/app_db"
    CLIP_MODEL_NAME: str = "openai/clip-vit-base-patch32"

    class Config:
        env_file = ".env"

settings = Settings()