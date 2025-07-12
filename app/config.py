from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from app.config import settings  # Import settings from config module


class Settings(BaseSettings):
    

    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

    if SQLALCHEMY_DATABASE_URL is None:
    # fallback to local settings if DATABASE_URL not found (for local development)
         SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

    
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "CHACHU2206"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    secret_key: str = "secretkey1010101"  # Example secret key for JWT
    algorithm: str = "HS256"  # Example algorithm for JWT
    access_token_expire_minutes: int = 60  # Token expiration time in minutes

    model_config = SettingsConfigDict(env_file=".env")


settings= Settings()  # Create an instance of Settings with default values