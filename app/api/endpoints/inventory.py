from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api import deps
from app.core.db import get_session
from app.models.stock import Product, StockMovement
from app.services.stock import StockService

router = APIRouter()


@router.get("/products", response_model=List[Product])
def read_products(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    products = db.exec(select(Product).offset(skip).limit(limit)).all()
    return products


@router.post("/movement")
def create_movement(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    warehouse_id: int,
    quantity: int,
    type: str,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    try:
        product = StockService.process_movement(
            db=db,
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            movement_type=type,
            user_id=current_user.id
        )
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
