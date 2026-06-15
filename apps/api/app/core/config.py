from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Servicios Pinturas Starcolors"
    app_env: str = "development"
    debug: bool = False 
    api_version: str = "0.1.0"
    database_url: str = ""
    jwt_secret_key: str = "dev_change_me_secret_key_32_chars_minimum"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 6 
    backend_cors_origins: list[str] = [
        "http://localhost:4321",
        "http://127.0.0.1:4321",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # SMTP Configuration
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from: str = "no-reply@starcolorsmx.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
