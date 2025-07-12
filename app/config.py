from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "CHACHU2206"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    secret_key: str = "secretkey1010101"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Strip whitespace from env vars in case Heroku added a trailing newline
settings.database_hostname = settings.database_hostname.strip()
settings.database_port = settings.database_port.strip()
settings.database_password = settings.database_password.strip()
settings.database_name = settings.database_name.strip()
settings.database_username = settings.database_username.strip()
