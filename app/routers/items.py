from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Item, ItemUpdate
from app.crud import get_item, get_items, create_item, update_item
from app.settings import get_db
from app.settings import redis_client
from fastapi.encoders import jsonable_encoder
import json

router = APIRouter()

@router.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    cached_item = redis_client.get(f"item:{item_id}")
    if cached_item:
        return {"item_id": item_id, "item": json.loads(cached_item)}

    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    serialized_item = jsonable_encoder(item)
    redis_client.setex(f"item:{item_id}", 3600, json.dumps(serialized_item))
    return {"item_id": item_id, "item": serialized_item}

@router.get("/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return {"skip": skip, "limit": limit, "items": items}

@router.post("/")
def create_new_item(item: Item, db: Session = Depends(get_db)):
    db_item = create_item(db, item)
    serialized_item = jsonable_encoder(db_item)
    redis_client.setex(f"item:{db_item.id}", 3600, json.dumps(serialized_item))
    return {"item_id": db_item.id, "item": serialized_item}

@router.patch("/{item_id}")
def update_existing_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = update_item(db, db_item, item)
    serialized_item = jsonable_encoder(updated_item)
    redis_client.set(f"item:{item_id}", json.dumps(serialized_item))
    return {"item_id": updated_item.id, "updated_item": serialized_item}
