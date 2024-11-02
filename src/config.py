import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', 5001))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    GRPC_RUN_PORT = int(os.getenv('GRPC_RUN_PORT', 50051))
