# app/settings.py
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings
import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    # Database configuration
    SQLALCHEMY_DATABASE_URL: str = "mysql+mysqlconnector://root:root%40123@localhost/mydatabase"
    
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Application settings
    SECRET_KEY: str = "your-secret-key"
    DEBUG: bool = True
    CACHE_TTL: int = 3600  # Default cache expiration time in seconds

    # Metadata
    APP_NAME: str = "My FastAPI App"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"  # Optional: Load settings from a .env file

# Instantiate the settings
settings = Settings()

# Database connection setup

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)  # Use the database URL from settings
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# Database dependency (usually in dependencies.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Redis client setup
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Redis health check function 
def check_redis_health():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False        