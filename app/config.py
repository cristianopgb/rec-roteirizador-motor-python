from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rec-roteirizador-motor-python"
    app_version: str = "1.0.0"
    debug: bool = False

    # Configurações da API
    api_prefix: str = "/api/v1"

    # Configurações do pipeline
    max_workers: int = 4
    timeout_segundos: int = 300

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
