from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    item_id: int
    quantity: int
    name: str | None = None
    price: float | None = None

class OrderRead(BaseModel):
    id: UUID
    items: List[OrderItemRead]