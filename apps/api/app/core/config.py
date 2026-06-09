from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Servicios Pinturas Starcolors"
    app_env: str = "development"
    debug: bool = True
    api_version: str = "0.1.0"
    database_url: str = ""
    jwt_secret_key: str = "CHANGE_ME_TO_A_32_BYTE_SECRET_IN_ENV"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    backend_cors_origins: list[str] = [
        "http://localhost:4321",
        "http://127.0.0.1:4321",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
