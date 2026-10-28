import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "rythucrop-agri-decision-support-key-2026")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_PATH = BASE_DIR / "rythucrop.db"
    
    # Auth & OTP Settings
    DEV_AUTH_MODE = os.environ.get("RYTHUCROP_DEV_AUTH", "true").lower() == "true"
    OTP_VALIDITY_MINUTES = int(os.environ.get("OTP_VALIDITY_MINUTES", 5))
    OTP_MAX_ATTEMPTS = int(os.environ.get("OTP_MAX_ATTEMPTS", 3))
    OTP_COOLDOWN_SECONDS = int(os.environ.get("OTP_COOLDOWN_SECONDS", 60))
    SMS_API_KEY = os.environ.get("SMS_API_KEY", "")
    
    # ML Model Artifacts
    RECOMMENDATION_MODEL_PATH = BASE_DIR / "ml" / "saved_models" / "crop_recommendation_model.pkl"
    YIELD_MODEL_PATH = BASE_DIR / "ml" / "saved_models" / "crop_yield_model.pkl"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DEV_AUTH_MODE = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DEV_AUTH_MODE = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEV_AUTH_MODE = True
