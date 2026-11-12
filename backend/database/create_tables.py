from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

from backend.database.models import Base

# Load database settings
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create all database tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")