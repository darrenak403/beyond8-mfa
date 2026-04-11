from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

class Settings(BaseSettings):
    app_name: str = "Beyond8 Auth Service"
    api_prefix: str = Field(default="/api", alias="API_PREFIX")

    database_url: str = Field(default="", alias="DATABASE_URL")

    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = Field(default=52560000, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    course_access_token_expire_days: int = 30

    otp_ttl_seconds: int = 60
    otp_length: int = 6
    otp_refresh_cooldown_seconds: int = 60

    seed_admin_email: str = "admin@gmail.com"
    run_startup_bootstrap: bool = Field(default=True, alias="RUN_STARTUP_BOOTSTRAP")

    key_prefix: str = Field(default="BY8", alias="KEY_PREFIX")
    cors_origins: str = Field(
        default=(
            "http://127.0.0.1:5500,"
            "http://localhost:5500,"
            "https://source.beyond8.io.vn,"
            "https://mfa.beyond8.io.vn"
        ),
        alias="CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(env_file=_env_path, env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        normalized: List[str] = []
        for raw_item in self.cors_origins.split(","):
            candidate = raw_item.strip().strip("\"'").rstrip("/")
            if not candidate:
                continue
            if candidate not in normalized:
                normalized.append(candidate)
        return normalized


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
