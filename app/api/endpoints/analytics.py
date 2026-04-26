from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api import deps
from app.core.db import get_session
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/reports/turnover")
def get_turnover_report(
    db: Session = Depends(get_session),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    return AnalyticsService.get_stock_turnover_report(db)


@router.get("/reports/low-stock")
def get_low_stock_report(
    db: Session = Depends(get_session),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    return AnalyticsService.get_low_stock_summary(db)


@router.get("/reports/warehouse-utilization")
def get_utilization_report(
    db: Session = Depends(get_session),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    return AnalyticsService.get_warehouse_utilization(db)
