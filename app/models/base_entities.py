from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class WarehouseBase(SQLModel):
    name: str = Field(index=True)
    location: Optional[str] = None


class Warehouse(WarehouseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    inventory: List["Inventory"] = Relationship(back_populates="warehouse")
    movements: List["StockMovement"] = Relationship(back_populates="warehouse")


class SupplierBase(SQLModel):
    name: str = Field(index=True)
    contact_email: Optional[str] = None
    phone: Optional[str] = None


class Supplier(SupplierBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    products: List["Product"] = Relationship(back_populates="supplier")
