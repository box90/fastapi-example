
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from src.models import OrderCreate, OrderItemRead, OrderRead
from src.routers import items, orders
from src.db import ItemBase, ItemModel, OrderItem, OrderModel, SessionDep, create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(orders.router)
app.include_router(items.router)