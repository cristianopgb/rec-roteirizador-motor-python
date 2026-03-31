"""
M2 - Enriquecimento
Enriquece as entregas com dados adicionais: geocodificação, distâncias à base, etc.
"""
from typing import Any, Dict

from app.utils.geo import calcular_distancia_km
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enriquece cada entrega calculando a distância em linha reta até a base de cada veículo
    e armazena no metadata da entrega para uso posterior no pipeline.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto com entregas enriquecidas.
    """
    entregas = contexto.get("entregas", [])
    veiculos = contexto.get("veiculos", [])

    if not veiculos:
        logger.warning("M2: nenhum veículo disponível para calcular distâncias.")
        return contexto

    base_lat = veiculos[0].base_latitude
    base_lon = veiculos[0].base_longitude

    enriquecidas = 0
    for entrega in entregas:
        if entrega.endereco.latitude is not None and entrega.endereco.longitude is not None:
            dist = calcular_distancia_km(
                base_lat,
                base_lon,
                entrega.endereco.latitude,
                entrega.endereco.longitude,
            )
            # Armazena no contexto para uso nas próximas etapas
            if "distancias_base" not in contexto["metadata"]:
                contexto["metadata"]["distancias_base"] = {}
            contexto["metadata"]["distancias_base"][entrega.id] = round(dist, 3)
            enriquecidas += 1

    logger.debug("M2: %d/%d entregas enriquecidas com distância à base.", enriquecidas, len(entregas))
    contexto["entregas"] = entregas
    return contexto
