from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://unievents:unievents@localhost:5432/unievents"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    ALGORITHM: str = "HS256"
    PORT: int = 8000
    CORS_ORIGINS: str = "*"
    DISABLE_DOCS: bool = False
    APPLE_BUNDLE_ID: str = "pl.startupstars.kozmindaily"
    FIREBASE_CREDENTIALS_JSON: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def async_database_url(self) -> str:
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

        url = self.DATABASE_URL
        # Neon/Railway give postgresql://, we need postgresql+asyncpg://
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Strip params that asyncpg handles via connect_args (ssl, channel_binding)
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            params.pop("sslmode", None)
            params.pop("channel_binding", None)
            cleaned_query = urlencode(params, doseq=True)
            url = urlunparse(parsed._replace(query=cleaned_query))
        return url


settings = Settings()
