from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_AUTH_SECRET:str=''
    JWT_AUTH_ALGORITHM: str = "HS256"
    API_VERSION:str=''
    REDIS_HOST:str='localhost'
    REDIS_PORT:int=6379

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

config = Settings()

