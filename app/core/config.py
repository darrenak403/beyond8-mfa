from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Beyond8 Auth Service"
    api_prefix: str = Field(default="/api", alias="API_PREFIX")

    database_url: str = Field(default="", alias="DATABASE_URL")

    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    course_access_token_expire_days: int = 30

    otp_ttl_seconds: int = 60
    otp_length: int = 6
    otp_refresh_cooldown_seconds: int = 60

    seed_admin_email: str = "admin@gmail.com"

    key_prefix: str = Field(default="BY8", alias="KEY_PREFIX")
    cors_origins: str = Field(default="http://127.0.0.1:5500,http://localhost:5500", alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @property
    def cors_origins_list(self) -> List[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
