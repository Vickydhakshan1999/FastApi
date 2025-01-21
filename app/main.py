from fastapi import FastAPI
# from app.database import Base, engine
from app.routers import items, health
from app.settings import Base, engine, settings 

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(health.router, prefix="/health", tags=["health"])

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}
