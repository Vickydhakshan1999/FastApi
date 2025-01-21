from sqlalchemy import Column, Integer, String, Float
from app.settings import Base

class ItemInDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), default=None)
    price = Column(Float)
    tax = Column(Float, default=None)
    Gst = Column(Float)
    new_column = Column(String)
