from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from fastapi import Depends
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

class ItemBase(SQLModel):
    name: str = Field(index=True)
    price: float = Field(index=True)
    is_offer: bool | None = Field(default=False)


class ItemModel(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orders: List["OrderItem"] = Relationship(back_populates="item")

class OrderModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    order_items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    order_id: UUID = Field(foreign_key="ordermodel.id", primary_key=True)
    item_id: int = Field(foreign_key="itemmodel.id", primary_key=True)
    quantity: int = Field(default=1)

    order: "OrderModel" = Relationship(back_populates="order_items")
    item: "ItemModel" = Relationship(back_populates="orders")



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
