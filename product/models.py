from sqlalchemy import Column, Integer, String, Float, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from connect import Base

class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=True)
    item_description = Column(String) 
    item_quantity = Column(String)
    item_price = Column(Float, nullable=True)
    category = Column(String)
    manufacture_date = Column(Date)
    expiry_date = Column(Date)
    units = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String, server_default="Active")
    last_updated_by = Column(String)
    discount = Column(Float)

class Category(Base):
    __tablename__ = "categorys"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=True, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String)
   
    
class Offer(Base):
    __tablename__ = "offers"
    offer_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer)
    discount = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String)

