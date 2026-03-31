from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.roteirizacao import router as roteirizacao_router
from app.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(roteirizacao_router)
