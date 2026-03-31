"""
M9 - Consolidação
Consolida os resultados do pipeline: ordena rotas, calcula totais globais
e prepara o contexto final para a camada de resposta.
"""
from typing import Any, Dict, List

from app.schemas import Rota
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Consolida e finaliza o pipeline:
    - Ordena rotas por veículo
    - Calcula métricas globais
    - Adiciona mensagem de status

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto final pronto para resposta da API.
    """
    rotas: List[Rota] = contexto.get("rotas", [])
    sobras = contexto.get("sobras", [])

    # Ordena rotas por ID do veículo para saída consistente
    rotas.sort(key=lambda r: r.veiculo_id)

    total_entregas = contexto.get("total_entregas", 0)
    total_roteirizadas = sum(len(r.paradas) for r in rotas)
    total_sobras = len(sobras)

    contexto["metadata"]["resumo"] = {
        "total_entregas": total_entregas,
        "entregas_roteirizadas": total_roteirizadas,
        "entregas_nao_roteirizadas": total_sobras,
        "total_rotas": len(rotas),
        "distancia_total_km": round(sum(r.distancia_total_km for r in rotas), 3),
        "tempo_total_min": round(sum(r.tempo_total_min for r in rotas), 1),
    }

    if total_sobras == 0:
        mensagem = "Todas as entregas foram roteirizadas com sucesso."
    elif total_roteirizadas == 0:
        mensagem = "Nenhuma entrega foi roteirizada. Verifique a configuração dos veículos."
    else:
        mensagem = (
            f"{total_roteirizadas} de {total_entregas} entrega(s) roteirizada(s). "
            f"{total_sobras} entrega(s) sem rota."
        )

    contexto["rotas"] = rotas
    contexto["mensagem"] = mensagem

    logger.info("M9: consolidação concluída — %s", mensagem)
    return contexto
