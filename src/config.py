"""Настройки приложения для доставки еды."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Хранит конфигурацию приложения."""

    app_name: str = "Food Delivery App"
    debug: bool = False
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    database_url: str = "sqlite:///./food_delivery.db"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_prefix="FOOD_DELIVERY_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
