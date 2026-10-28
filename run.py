import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically load environment variables from .env in project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from app import app

if __name__ == "__main__":
    app.run(debug=False)
