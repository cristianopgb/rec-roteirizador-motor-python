from typing import Any, Dict, List

from app.schemas import RoteirizacaoRequest
from app.utils.logs import get_logger

logger = get_logger(__name__)


def validar_request(request: RoteirizacaoRequest) -> List[str]:
    """
    Valida a integridade da requisição antes de iniciar o pipeline.

    Returns:
        Lista de mensagens de erro; vazia se a requisição for válida.
    """
    erros: List[str] = []

    if not request.entregas:
        erros.append("A lista de entregas não pode ser vazia.")

    if not request.veiculos:
        erros.append("A lista de veículos não pode ser vazia.")

    veiculos_disponiveis = [v for v in request.veiculos if v.disponivel]
    if not veiculos_disponiveis:
        erros.append("Nenhum veículo disponível para a roteirização.")

    ids_entregas: List[str] = [e.id for e in request.entregas]
    if len(ids_entregas) != len(set(ids_entregas)):
        erros.append("Existem IDs de entrega duplicados.")

    ids_veiculos: List[str] = [v.id for v in request.veiculos]
    if len(ids_veiculos) != len(set(ids_veiculos)):
        erros.append("Existem IDs de veículo duplicados.")

    for entrega in request.entregas:
        if entrega.peso_kg <= 0 and entrega.volume_m3 <= 0:
            erros.append(f"Entrega '{entrega.id}' deve ter peso ou volume maior que zero.")

    if erros:
        logger.warning("Validação falhou com %d erro(s): %s", len(erros), erros)

    return erros
