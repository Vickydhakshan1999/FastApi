
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
# from typing import Optional

# # FastAPI app instance
# app = FastAPI()

# # Database URL 
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root%40123@localhost/mydatabase"


# # Set up the SQLAlchemy engine and session
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Declare the base class for models
# Base = declarative_base()

# # Define the Item model for the database
# class ItemInDB(Base):
#     __tablename__ = 'items'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), index=True)  # Specify length for VARCHAR
#     description = Column(String(255), default=None)
#     price = Column(Float)
#     tax = Column(Float, default=None)
#     Gst = Column(Float)

# # Create the database tables
# Base.metadata.create_all(bind=engine)

# # Define the Pydantic model for validation
# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None
#     Gst: float

#     class Config:
#         orm_mode = True

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, db: Session = Depends(get_db)):
#     item = db.query(ItemInDB).filter(ItemInDB.id == item_id).first()
#     if item:
#         return {"item_id": item.id, "item": item}
#     return {"message": "Item not found"}

# @app.get("/items/")
# def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     items = db.query(ItemInDB).offset(skip).limit(limit).all()
#     return {"skip": skip, "limit": limit, "items": items}

# @app.post("/items/")
# def create_item(item: Item, db: Session = Depends(get_db)):
#     db_item = ItemInDB(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return {"item_id": db_item.id, "item": db_item}


# # Define the model for PATCH requests
# class ItemUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     tax: Optional[float] = None
#     Gst: Optional[float] = None

# @app.patch("/items/{item_id}")
# def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
#     # Fetch the item from the database
#     db_item = db.query(ItemInDB).filter(ItemInDB.id == item_id).first()
    
#     # If the item does not exist, return a 404 error
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")

#     # Update only the provided fields
#     update_data = item.dict(exclude_unset=True)  # Exclude fields not provided in the request
#     for key, value in update_data.items():
#         setattr(db_item, key, value)  # Update the fields dynamically

#     # Commit the changes
#     db.commit()
#     db.refresh(db_item)  # Refresh to get the updated data

#     return {"item_id": db_item.id, "updated_item": db_item}




import json
import redis
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional

# FastAPI app instance
app = FastAPI()

# Database URL (MySQL)
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root%40123@localhost/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Define the Item model for the database
class ItemInDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)  # Specify length for VARCHAR
    description = Column(String(255), default=None)
    price = Column(Float)
    tax = Column(Float, default=None)
    Gst = Column(Float)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define the Pydantic model for validation
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    Gst: float

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None
    Gst: Optional[float] = None

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    # Check if item exists in Redis
    cached_item = redis_client.get(f"item:{item_id}")
    if cached_item:
        return {"item_id": item_id, "item": eval(cached_item)}

    # If not in Redis, fetch from DB
    item = db.query(ItemInDB).filter(ItemInDB.id == item_id).first()
    if not item:
        return {"message": "Item not found"}

    # Cache the item in Redis
    redis_client.set(f"item:{item_id}", item.json())
    return {"item_id": item.id, "item": item}

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(ItemInDB).offset(skip).limit(limit).all()
    return {"skip": skip, "limit": limit, "items": items}

@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    # Create a new item in the database
    db_item = ItemInDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Serialize and store the newly created item in Redis
    serialized_item = jsonable_encoder(db_item)  # Convert SQLAlchemy object to a JSON-serializable dict
    redis_client.set(f"item:{db_item.id}", json.dumps(serialized_item))  # Store as a JSON string

    return {"item_id": db_item.id, "item": serialized_item}
from fastapi.encoders import jsonable_encoder

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ItemInDB).filter(ItemInDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields dynamically
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)

    # Serialize and store in Redis
    serialized_item = jsonable_encoder(db_item)  # Converts to a JSON-serializable format
    redis_client.set(f"item:{db_item.id}", json.dumps(serialized_item))  # Store as JSON string

    return {"item_id": db_item.id, "updated_item": serialized_item}


# to check redis is connteced or not 

@app.get("/redis-health")
def redis_health():
    try:
        # Test Redis connection with a PING
        redis_client.ping()
        return {"status": "Redis is connected!"}
    except redis.ConnectionError:
        return {"status": "Failed to connect to Redis!"}


