import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings from environment variables"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'store')}"
    )
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API
    API_TITLE: str = os.getenv("API_TITLE", "Store Management API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "Enterprise-grade Store Management API designed to showcase backend architecture, business rules, and cloud-ready design.")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "to-be-changed-in-production-use-openssl-rand-hex-32")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

settings = Settings()
