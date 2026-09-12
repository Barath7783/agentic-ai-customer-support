import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.8-flash"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/customer_support"
)
