from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class ProductBase(SQLModel):
    sku: str = Field(unique=True, index=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    min_stock_level: int = 0
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    supplier: Optional["Supplier"] = Relationship(back_populates="products")
    inventory: List["Inventory"] = Relationship(back_populates="product")
    movements: List["StockMovement"] = Relationship(back_populates="product")


class Inventory(SQLModel, table=True):
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    warehouse_id: int = Field(foreign_key="warehouse.id", primary_key=True)
    quantity: int = 0
    
    product: "Product" = Relationship(back_populates="inventory")
    warehouse: "Warehouse" = Relationship(back_populates="inventory")


class StockMovementBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    quantity: int
    type: str # 'entry' or 'exit'
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class StockMovement(StockMovementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    product: "Product" = Relationship(back_populates="movements")
    warehouse: "Warehouse" = Relationship(back_populates="movements")
