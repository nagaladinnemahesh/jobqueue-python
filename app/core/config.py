import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "FastAPI App")
    ENV = os.getenv("ENV", "dev")
    PORT = int(os.getenv("PORT", 8000))

settings = Settings()