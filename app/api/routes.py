from fastapi import APIRouter
from app.api.endpoints import leads, health

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router)
api_router.include_router(leads.router) 