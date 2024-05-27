from fastapi import APIRouter

from app.routes.recommendations import router_auth

router: APIRouter = APIRouter()
router.include_router(router_auth)
