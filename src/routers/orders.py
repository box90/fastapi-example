from typing import List
from uuid import UUID
from db import ItemModel, OrderItem, OrderModel, SessionDep
from fastapi import APIRouter, HTTPException
from models import OrderCreate, OrderItemRead, OrderRead
from sqlmodel import select

router = APIRouter()

@router.get("/orders/", response_model=List[OrderModel] ,tags=["Orders"])
async def read_orders(session: SessionDep) -> List[OrderModel]:
    return session.exec(select(OrderModel)).all()

@router.post("/orders/", response_model=OrderModel ,tags=["Orders"])
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

@router.get("/orders/{order_id}", response_model=OrderRead ,tags=["Orders"])
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

@router.delete("/orders/{order_id}", status_code=204 ,tags=["Orders"])
async def delete_order(order_id: str, session: SessionDep):
    order_uuid = UUID(order_id)
    order = session.get(OrderModel, order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for oi in order.order_items:
        session.delete(oi)
    session.delete(order)
    session.commit()