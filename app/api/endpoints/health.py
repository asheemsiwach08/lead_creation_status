from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HOM-i Lead Creation & Status API",
        "version": "1.0.0",
        "endpoints": {
            "create_lead": "POST /api/v1/lead/create",
            "get_status": "POST /api/v1/lead/status"
        }
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "HOM-i Lead API"} 