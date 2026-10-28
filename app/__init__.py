import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rythucrop-agri-decision-support-key-2026")

from app.routes import main
from app.routes import prediction
from app.routes import api
