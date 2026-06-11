from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/jaemoney"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # JWT
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # SMTP (이메일)
    smtp_server: str = "smtp.sendgrid.net"
    smtp_port: int = 587
    smtp_username: str = "apikey"
    smtp_password: str = ""

    # 환경
    environment: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
