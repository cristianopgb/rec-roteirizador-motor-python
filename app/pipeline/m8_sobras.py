"""
M8 - Sobras
Processa as entregas que não foram alocadas em nenhuma rota, registrando
o motivo da não-alocação para relatório posterior.
"""
from typing import Any, Dict, List

from app.schemas import Entrega
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finaliza o tratamento das sobras, registrando diagnóstico de não-alocação.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto atualizado com sobras finalizadas.
    """
    sobras: List[Entrega] = contexto.get("sobras", [])
    veiculos = contexto.get("veiculos", [])

    diagnosticos: List[Dict[str, Any]] = []

    for entrega in sobras:
        motivo = _diagnosticar(entrega, veiculos, contexto)
        diagnosticos.append({"entrega_id": entrega.id, "motivo": motivo})
        logger.debug("M8: sobra '%s' — motivo: %s", entrega.id, motivo)

    contexto["metadata"]["sobras_diagnosticos"] = diagnosticos
    logger.info("M8: %d entregas sem rota registradas.", len(sobras))
    return contexto


def _diagnosticar(entrega: Entrega, veiculos: list, contexto: Dict[str, Any]) -> str:
    if entrega.endereco.latitude is None or entrega.endereco.longitude is None:
        return "sem_coordenada"

    if not veiculos:
        return "sem_veiculo_disponivel"

    max_cap_peso = max((v.capacidade_kg for v in veiculos), default=0)
    max_cap_vol = max((v.capacidade_m3 for v in veiculos), default=0)

    if entrega.peso_kg > max_cap_peso:
        return "excede_capacidade_peso"
    if entrega.volume_m3 > max_cap_vol:
        return "excede_capacidade_volume"

    parametros = contexto.get("parametros")
    if parametros and parametros.raio_max_km:
        dist = contexto.get("metadata", {}).get("distancias_base", {}).get(entrega.id, 0.0)
        if dist > parametros.raio_max_km:
            return "fora_do_raio"

    return "capacidade_esgotada"
