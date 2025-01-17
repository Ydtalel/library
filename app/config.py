from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация настроек приложения, загружаемая из файла .env"""

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
