
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import OrderCreate, OrderItemRead, OrderRead
from sqlmodel import select
from db import ItemBase, ItemModel, OrderItem, OrderModel, SessionDep, create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/items/")
async def read_elements(session: SessionDep) -> List[ItemModel]:
    return session.exec(select(ItemModel)).all()


@app.get("/items/{item_id}", response_model=ItemModel)
async def read_item(item_id: int, session: SessionDep) -> ItemModel:
    item = session.get(ItemModel,item_id)
    if not item:
         raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/",response_model=ItemModel)
async def create_item(item: ItemBase, session: SessionDep) -> ItemModel:
    model = ItemModel(**item.model_dump())
    session.add(model)
    session.commit()
    session.refresh(model)
    return 

# --- CRUD Orders ---

@app.get("/orders/", response_model=List[OrderModel])
async def read_orders(session: SessionDep) -> List[OrderModel]:
    return session.exec(select(OrderModel)).all()

@app.post("/orders/", response_model=OrderModel)
async def create_order(order: OrderCreate, session: SessionDep) -> OrderModel:
    db_order = OrderModel()
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    for item in order.items:
        db_order_item = OrderItem(order_id=db_order.id, item_id=item.item_id, quantity=item.quantity)
        session.add(db_order_item)
    session.commit()
    session.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderRead)
async def read_order(order_id: str, session: SessionDep) -> OrderRead:
    order_uuid = UUID(order_id)
    order = session.get(OrderModel, order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    items = []
    for oi in order.order_items:
        item = session.get(ItemModel, oi.item_id)
        items.append(OrderItemRead(
            item_id=oi.item_id,
            quantity=oi.quantity,
            name=item.name if item else None,
            price=item.price if item else None
        ))
    return OrderRead(id=order.id, items=items)

@app.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: str, session: SessionDep):
    order_uuid = UUID(order_id)
    order = session.get(OrderModel, order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for oi in order.order_items:
        session.delete(oi)
    session.delete(order)
    session.commit()