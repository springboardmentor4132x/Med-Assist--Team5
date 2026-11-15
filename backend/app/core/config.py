import os
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url


class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "MedAssist AI - Patient Profile Management"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # PostgreSQL Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "medassist_db"
    DATABASE_URL: str = ""

    # JWT Authentication Configuration
    SECRET_KEY: str = Field(
        default="medassist_development_super_secret_jwt_key_replace_in_prod_1234567890",
        description="Secret key used for signing JWT tokens"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            "backend/.env",
            os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"),
        ],
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str, info) -> str:
        data = info.data
        user = data.get("POSTGRES_USER", "postgres")
        password = data.get("POSTGRES_PASSWORD", "postgres")
        server = data.get("POSTGRES_SERVER", "localhost")
        port = data.get("POSTGRES_PORT", 5432)
        db = data.get("POSTGRES_DB", "medassist_db")

        # If explicit DATABASE_URL is provided:
        if isinstance(v, str) and v.strip():
            url_str = v.strip()
            try:
                parsed = make_url(url_str)
                # If host was parsed incorrectly due to unescaped characters in password (e.g. host == '20@localhost'):
                if parsed.host and "@" in parsed.host:
                    return URL.create(
                        "postgresql+psycopg2",
                        username=user,
                        password=password,
                        host=server,
                        port=int(port),
                        database=db
                    ).render_as_string(hide_password=False)
                return url_str
            except Exception:
                pass

        # Build safely using SQLAlchemy URL.create
        return URL.create(
            "postgresql+psycopg2",
            username=user,
            password=password,
            host=server,
            port=int(port),
            database=db
        ).render_as_string(hide_password=False)

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, str) and v.startswith("["):
            import json
            try:
                return json.loads(v)
            except Exception:
                return ["http://localhost:5173", "http://127.0.0.1:5173"]
        return v


settings = Settings()
