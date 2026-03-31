"""
M1 - Padronização
Normaliza e padroniza os dados de entregas e veículos (CEPs, strings, coordenadas).
"""
from typing import Any, Dict

from app.utils.logs import get_logger
from app.utils.numbers import arredondar

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padroniza os dados de entrada:
    - Normaliza strings de endereço (strip + upper)
    - Arredonda pesos e volumes
    - Remove CEPs com formatação inconsistente

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto atualizado com dados padronizados.
    """
    entregas = contexto.get("entregas", [])

    for entrega in entregas:
        entrega.endereco.logradouro = entrega.endereco.logradouro.strip().upper()
        entrega.endereco.cidade = entrega.endereco.cidade.strip().upper()
        entrega.endereco.estado = entrega.endereco.estado.strip().upper()

        if entrega.endereco.cep:
            entrega.endereco.cep = entrega.endereco.cep.replace("-", "").replace(".", "").strip()

        entrega.peso_kg = arredondar(entrega.peso_kg, 3)
        entrega.volume_m3 = arredondar(entrega.volume_m3, 4)

    logger.debug("M1: %d entregas padronizadas.", len(entregas))
    contexto["entregas"] = entregas
    return contexto
