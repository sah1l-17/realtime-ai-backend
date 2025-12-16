import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Realtime AI Backend"
    ENV = os.getenv("ENV", "dev")

settings = Settings()
