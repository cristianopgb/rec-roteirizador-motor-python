from fastapi import APIRouter, HTTPException

from app.schemas import RoteirizacaoRequest, RoteirizacaoResponse
from app.services.pipeline_service import executar_pipeline
from app.services.response_service import construir_resposta
from app.services.validation_service import validar_request
from app.utils.logs import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["roteirizacao"])


@router.post("/roteirizacao", response_model=RoteirizacaoResponse)
async def roteirizar(request: RoteirizacaoRequest) -> RoteirizacaoResponse:
    """Executa o pipeline de roteirização para a carga e frota fornecidas."""
    logger.info(
        "Iniciando roteirização: %d entregas, %d veículos",
        len(request.entregas),
        len(request.veiculos),
    )

    erros = validar_request(request)
    if erros:
        raise HTTPException(status_code=422, detail=erros)

    try:
        resultado = executar_pipeline(request)
    except Exception as exc:
        logger.exception("Erro inesperado no pipeline: %s", exc)
        raise HTTPException(status_code=500, detail="Erro interno no pipeline de roteirização.") from exc

    resposta = construir_resposta(resultado)
    logger.info(
        "Roteirização concluída: %d rotas geradas, %d sobras",
        len(resposta.rotas),
        len(resposta.sobras),
    )
    return resposta
