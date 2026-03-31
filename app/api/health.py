from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Verifica se a aplicação está em execução."""
    return HealthResponse(
        status="ok",
        versao=settings.app_version,
        timestamp=datetime.now(tz=timezone.utc),
    )
