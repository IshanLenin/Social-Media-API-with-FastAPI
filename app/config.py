from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "CHACHU2206"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    secret_key: str = "mysecretkey"  # Example secret key for JWT
    algorithm: str = "HS256"  # Example algorithm for JWT
    access_token_expire_minutes: int = 30  # Token expiration time in minutes

    model_config = SettingsConfigDict(env_file=".env")


settings= Settings()  # Create an instance of Settings with default values