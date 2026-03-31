from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.roteirizacao import router as roteirizacao_router
from app.config import settings
from app.utils.logs import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Aplicação iniciada: %s v%s", settings.app_name, settings.app_version)
    yield
    logger.info("Aplicação encerrada.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Motor de cálculo de roteirização para logística.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(roteirizacao_router, prefix=settings.api_prefix)
