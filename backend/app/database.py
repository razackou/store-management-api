import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment or construct it from components
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'store')}",
)

# Determine if we're in production (using RDS or similar)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# Configure engine based on environment
engine_kwargs = {
    "echo": os.getenv("SQL_ECHO", "False").lower() == "true",
}

# For cloud databases (AWS RDS, etc.), use connection pooling
# For local development, use NullPool to avoid connection issues
if ENVIRONMENT == "production":
    # Production: Use QueuePool with SSL and connection pooling
    engine_kwargs["poolclass"] = QueuePool
    engine_kwargs["pool_size"] = int(os.getenv("DB_POOL_SIZE", "10"))
    engine_kwargs["max_overflow"] = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    engine_kwargs["pool_pre_ping"] = True  # Test connections before using
    engine_kwargs["pool_recycle"] = 3600  # Recycle connections every hour

    # Add SSL for cloud databases
    if "sslmode" not in DATABASE_URL:
        DATABASE_URL = f"{DATABASE_URL}?sslmode=require"
else:
    # Development: Use NullPool to avoid connection issues
    engine_kwargs["poolclass"] = NullPool

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
