from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = Field(default='REC Motor Python', alias='APP_NAME')
    app_env: str = Field(default='development', alias='APP_ENV')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')
    port: int = Field(default=10000, alias='PORT')


settings = Settings()
