from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    API_FOOTBALL_KEY: str
    CHROMA_COLLECTION_NAME: str = "sports_betting"

    LANGSMITH_TRACING: bool = False
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "matchsense"

    class Config:
        env_file = ".env"

settings = Settings()