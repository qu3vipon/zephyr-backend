from fastapi import FastAPI

from .api.api_v1.routers import api_router
from .core.config import settings

app = FastAPI(
    title="Zephyr",
    contact={"name": "qu3vipon", "email": "qu3vipon@gmail.com"},
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
