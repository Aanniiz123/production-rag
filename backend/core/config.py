from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    GROQ_API_KEY: str
    # Frontend URL
    FRONTEND_URL: str
    # Google OAuth settings
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"



settings = Settings()