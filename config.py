import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "portfolio_secret_key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///portfolio.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folders
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    PROFILE_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "profile")

    RESUME_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "resume")

    CERTIFICATE_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "certificates")

    PROJECT_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "projects")