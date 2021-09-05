from fastapi import APIRouter

from zephyr.app.api.api_v1.endpoints import auth, search, user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
