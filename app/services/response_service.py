from typing import Any, Dict

from app.schemas import EstatisticasRoteirizacao, RoteirizacaoResponse
from app.utils.logs import get_logger

logger = get_logger(__name__)


def construir_resposta(resultado: Dict[str, Any]) -> RoteirizacaoResponse:
    """
    Constrói o objeto de resposta a partir do contexto retornado pelo pipeline.

    Args:
        resultado: Dicionário de contexto gerado pelo pipeline.

    Returns:
        RoteirizacaoResponse pronto para ser serializado pela API.
    """
    rotas = resultado.get("rotas", [])
    sobras = resultado.get("sobras", [])

    total_entregas = resultado.get("total_entregas", 0)
    entregas_roteirizadas = sum(len(r.paradas) for r in rotas)
    entregas_nao_roteirizadas = len(sobras)

    distancia_total = sum(r.distancia_total_km for r in rotas)
    tempo_total = sum(r.tempo_total_min for r in rotas)

    estatisticas = EstatisticasRoteirizacao(
        total_entregas=total_entregas,
        entregas_roteirizadas=entregas_roteirizadas,
        entregas_nao_roteirizadas=entregas_nao_roteirizadas,
        total_rotas=len(rotas),
        distancia_total_km=round(distancia_total, 2),
        tempo_total_min=round(tempo_total, 2),
    )

    return RoteirizacaoResponse(
        status="sucesso",
        mensagem=resultado.get("mensagem", "Roteirização concluída com sucesso."),
        rotas=rotas,
        sobras=sobras,
        estatisticas=estatisticas,
        metadata=resultado.get("metadata", {}),
    )
