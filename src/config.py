import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TRANSLATION_SERVICE_PORT = os.getenv("TRANSLATION_SERVICE_PORT", "50051")
