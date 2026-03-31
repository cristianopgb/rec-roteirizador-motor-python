"""
M3.1 - Fronteira
Processa as entregas classificadas como fronteira (fora do raio principal),
decidindo se devem ser roteirizadas em rota especial ou descartadas como sobras.
"""
from typing import Any, Dict, List

from app.schemas import Entrega
from app.utils.logs import get_logger

logger = get_logger(__name__)

LIMITE_FRONTEIRA_KM = 50.0


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Trata as entregas de fronteira:
    - Entregas dentro do limite secundário são mantidas para roteirização.
    - Entregas além do limite secundário são movidas para sobras.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto atualizado.
    """
    grupos = contexto.get("grupos", {})
    fronteira: List[Entrega] = grupos.get("fronteira", [])
    distancias_base: Dict[str, float] = contexto.get("metadata", {}).get("distancias_base", {})

    aceitas: List[Entrega] = []
    sobras: List[Entrega] = []

    for entrega in fronteira:
        dist = distancias_base.get(entrega.id, 0.0)
        if dist <= LIMITE_FRONTEIRA_KM:
            aceitas.append(entrega)
        else:
            sobras.append(entrega)
            logger.debug("M3.1: entrega '%s' (%.1f km) movida para sobras.", entrega.id, dist)

    # Retorna as aceitas ao grupo normal para continuar no pipeline
    grupos["normal"].extend(aceitas)
    grupos["fronteira"] = []

    contexto["grupos"] = grupos
    contexto["sobras"].extend(sobras)

    logger.debug(
        "M3.1: %d entregas de fronteira aceitas, %d para sobras.",
        len(aceitas),
        len(sobras),
    )
    return contexto
