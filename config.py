import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_generated_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mesh_ai.db'  # Using SQLite for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False
