"""
M5.1 - Saneamento
Verifica e corrige inconsistências nas rotas geradas: sequência de paradas,
cálculos de distância e tempo, e dados obrigatórios.
"""
from typing import Any, Dict, List

from app.schemas import Rota
from app.utils.geo import calcular_distancia_km
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitiza as rotas recalculando sequência, distâncias e tempos.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto com rotas saneadas.
    """
    rotas: List[Rota] = contexto.get("rotas", [])

    for rota in rotas:
        dist_total = 0.0
        tempo_total = 0.0

        for idx, parada in enumerate(rota.paradas):
            parada.sequencia = idx + 1

            if idx > 0:
                prev = rota.paradas[idx - 1]
                if (
                    prev.endereco.latitude is not None
                    and prev.endereco.longitude is not None
                    and parada.endereco.latitude is not None
                    and parada.endereco.longitude is not None
                ):
                    dist = calcular_distancia_km(
                        prev.endereco.latitude,
                        prev.endereco.longitude,
                        parada.endereco.latitude,
                        parada.endereco.longitude,
                    )
                    parada.distancia_anterior_km = round(dist, 3)
                    # Estimativa de velocidade média 40 km/h
                    parada.tempo_estimado_min = round((dist / 40) * 60, 1)
                else:
                    parada.distancia_anterior_km = 0.0
                    parada.tempo_estimado_min = 0.0
            else:
                parada.distancia_anterior_km = 0.0
                parada.tempo_estimado_min = 0.0

            dist_total += parada.distancia_anterior_km
            tempo_total += parada.tempo_estimado_min

        rota.distancia_total_km = round(dist_total, 3)
        rota.tempo_total_min = round(tempo_total, 1)

    logger.debug("M5.1: %d rotas saneadas.", len(rotas))
    contexto["rotas"] = rotas
    return contexto
