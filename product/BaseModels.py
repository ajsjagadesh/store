from pydantic import BaseModel, EmailStr
from datetime import datetime

class Item(BaseModel):
    item_name: str
    item_description: str
    item_quantity: str
    item_price: float
    category: str
    manufacture_date: datetime
    expiry_date: datetime
    units: int
    discount: float

class Category(BaseModel):
    category_name: str

class Offers(BaseModel):
    item_id: int
    discount: float

class add_item(BaseModel):
    message: str
    item_name: str
