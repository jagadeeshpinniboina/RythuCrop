import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically load environment variables from .env in project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rythucrop-agri-decision-support-key-2026")

from app.routes.auth import auth_bp
app.register_blueprint(auth_bp)

from app.routes import main
from app.routes import prediction
from app.routes import api
from app.routes import advisory
