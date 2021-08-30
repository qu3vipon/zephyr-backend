from fastapi import FastAPI, Depends

from .api.api_v1.routers import api_router
from .core.config import get_settings, Settings, settings

app = FastAPI()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.ENVIRONMENT,
        "testing": settings.TESTING
    }


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
