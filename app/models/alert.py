from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class AlertBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    type: str  # 'low_stock' or 'rupture'
    message: str
    is_resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Alert(AlertBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
