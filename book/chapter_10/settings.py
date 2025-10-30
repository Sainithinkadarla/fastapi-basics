from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    db_url: str
    environment: str

    class Config:
        env_file = ".env"

settings = Settings()