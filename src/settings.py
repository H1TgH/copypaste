from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BaseSettings.model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow"
)


class RedisSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_prefix="REDIS_"
    )


class Settings(BaseSettings):
    redis: RedisSettings = Field(default_factory=RedisSettings)


settings = Settings()
