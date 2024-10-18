from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for FastAPI
class ProductBase(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: str

    class Config:
        orm_mode = True  # Important for Pydantic to work with ORM objects