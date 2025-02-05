from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "The Crate"
    API_V1_STR: str = "/api/v1"

    # CORS Configuration
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173"]

    user: str
    password: str
    host: str
    port: str
    dbname: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Python Settings
    PYTHONDONTWRITEBYTECODE: str = "1"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
