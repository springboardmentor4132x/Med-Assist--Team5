from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

db_url = settings.DATABASE_URL
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(db_url, connect_args=connect_args)
    # Test connection
    with engine.connect() as conn:
        pass
except Exception as e:
    # If PostgreSQL connection fails (e.g. service not started yet), safely fallback to local sqlite
    print(f"[Warning] Failed connecting to configured database ({db_url}): {e}")
    print("[Info] Falling back to SQLite for seamless local execution (sqlite:///./medassist.db)...")
    fallback_url = "sqlite:///./medassist.db"
    engine = create_engine(fallback_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
