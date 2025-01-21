from sqlalchemy.orm import Session
from .models import ItemInDB
from .schemas import Item, ItemUpdate

def get_item(db: Session, item_id: int):
    return db.query(ItemInDB).filter(ItemInDB.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ItemInDB).offset(skip).limit(limit).all()

def create_item(db: Session, item: Item):
    db_item = ItemInDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: ItemInDB, item: ItemUpdate):
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item
