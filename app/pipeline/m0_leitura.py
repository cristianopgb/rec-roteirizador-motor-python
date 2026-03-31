"""
M0 - Leitura
Responsável por carregar e estruturar os dados de entrada no contexto do pipeline.
"""
from typing import Any, Dict

from app.schemas import RoteirizacaoRequest
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(request: RoteirizacaoRequest) -> Dict[str, Any]:
    """
    Carrega a requisição e inicializa o contexto do pipeline.

    Args:
        request: Dados de entrada da API.

    Returns:
        Contexto inicial do pipeline.
    """
    logger.debug("M0: carregando %d entregas e %d veículos.", len(request.entregas), len(request.veiculos))

    contexto: Dict[str, Any] = {
        "entregas": list(request.entregas),
        "veiculos": [v for v in request.veiculos if v.disponivel],
        "parametros": request.parametros,
        "total_entregas": len(request.entregas),
        "rotas": [],
        "sobras": [],
        "metadata": {},
    }

    return contexto
