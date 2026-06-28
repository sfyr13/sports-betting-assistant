from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    API_FOOTBALL_KEY: str
    CHROMA_COLLECTION_NAME: str = "sports_betting"

    class Config:
        env_file = ".env"

settings = Settings()

