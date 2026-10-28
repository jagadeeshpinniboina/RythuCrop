import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rythucrop-agri-decision-support-key-2026")

from app.routes.auth import auth_bp
app.register_blueprint(auth_bp)

from app.routes import main
from app.routes import prediction
from app.routes import api
