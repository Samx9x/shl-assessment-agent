import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
)

CHROMA_DB_DIR = os.path.join(
    DATA_DIR,
    "chroma_db",
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)