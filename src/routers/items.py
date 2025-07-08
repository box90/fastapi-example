from typing import List
from db import ItemBase, ItemModel, SessionDep
from fastapi import APIRouter, HTTPException
from sqlmodel import select

router = APIRouter()


@router.get("/items/", tags=["Items"])
async def read_elements(session: SessionDep) -> List[ItemModel]:
    return session.exec(select(ItemModel)).all()


@router.get("/items/{item_id}", tags=["Items"])
async def read_item(item_id: int, session: SessionDep) -> ItemModel:
    item = session.get(ItemModel,item_id)
    if not item:
         raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items/",tags=["Items"])
async def create_item(item: ItemBase, session: SessionDep) -> ItemModel:
    model = ItemModel(**item.model_dump())
    session.add(model)
    session.commit()
    session.refresh(model)
    return model