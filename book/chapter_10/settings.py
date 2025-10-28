from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    myvar: str

    class Config:
        env_file = ".env"

settings = Settings()