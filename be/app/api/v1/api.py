from fastapi import APIRouter

from app.api.v1.endpoints import auth, dashboard, otp, stats

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(otp.router)
api_router.include_router(stats.router)
api_router.include_router(dashboard.router)
