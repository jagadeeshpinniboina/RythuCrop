import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically load environment variables from .env in project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from app import app

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host=host, port=port, debug=debug, threaded=True)
