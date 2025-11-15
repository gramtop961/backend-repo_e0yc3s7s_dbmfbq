from pydantic import BaseModel, Field
from typing import Optional, List

# Each model maps to a MongoDB collection with the lowercase class name

class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    cover_image: Optional[str] = None
    tags: List[str] = []

class Message(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str

class Product(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    category: str # outdoor, indoor, seasonal, decor, supplies
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    in_stock: Optional[bool] = True
