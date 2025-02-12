from app import app
from models import db

with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Recreate tables based on the updated models
    print("Database initialized successfully!")