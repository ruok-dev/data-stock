from fastapi import APIRouter
from app.api.endpoints import login, inventory, analytics

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
