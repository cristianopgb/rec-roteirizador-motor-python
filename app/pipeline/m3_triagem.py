"""
M3 - Triagem
Classifica as entregas em grupos: dentro do raio permitido, fora do raio (fronteira),
janela de tempo inválida, etc.
"""
from typing import Any, Dict, List

from app.schemas import Entrega
from app.utils.logs import get_logger

logger = get_logger(__name__)

GRUPO_NORMAL = "normal"
GRUPO_FRONTEIRA = "fronteira"
GRUPO_SEM_COORDENADA = "sem_coordenada"
GRUPO_FORA_JANELA = "fora_janela"


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Triagem das entregas, separando-as em grupos para processamento especializado.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto com campo 'grupos' populado.
    """
    entregas: List[Entrega] = contexto.get("entregas", [])
    parametros = contexto.get("parametros")
    distancias_base: Dict[str, float] = contexto.get("metadata", {}).get("distancias_base", {})

    grupos: Dict[str, List[Entrega]] = {
        GRUPO_NORMAL: [],
        GRUPO_FRONTEIRA: [],
        GRUPO_SEM_COORDENADA: [],
        GRUPO_FORA_JANELA: [],
    }

    raio_max = parametros.raio_max_km if parametros else None

    for entrega in entregas:
        if entrega.endereco.latitude is None or entrega.endereco.longitude is None:
            grupos[GRUPO_SEM_COORDENADA].append(entrega)
            continue

        dist = distancias_base.get(entrega.id)
        if raio_max is not None and dist is not None and dist > raio_max:
            grupos[GRUPO_FRONTEIRA].append(entrega)
            continue

        grupos[GRUPO_NORMAL].append(entrega)

    contagens = {k: len(v) for k, v in grupos.items()}
    logger.debug("M3: triagem concluída — %s", contagens)

    contexto["grupos"] = grupos
    return contexto
