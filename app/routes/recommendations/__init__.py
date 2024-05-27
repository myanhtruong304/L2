from fastapi import APIRouter

from app.routes.recommendations import recommendation_api

router_auth: APIRouter = APIRouter()
router_auth.include_router(recommendation_api.router, tags=["Authentication"])
