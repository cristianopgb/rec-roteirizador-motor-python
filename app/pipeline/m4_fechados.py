"""
M4 - Fechados
Monta rotas "fechadas": cada veículo recebe um conjunto de entregas agrupadas
por proximidade, respeitando as capacidades do veículo.
"""
from typing import Any, Dict, List

from app.schemas import Entrega, ParadaRota, Rota, Veiculo
from app.utils.geo import calcular_distancia_km
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cria rotas fechadas atribuindo entregas aos veículos disponíveis.

    A lógica básica distribui as entregas em ordem de distância à base,
    respeitando capacidade de peso e volume.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto com campo 'rotas' populado.
    """
    grupos = contexto.get("grupos", {})
    entregas: List[Entrega] = grupos.get("normal", [])
    veiculos: List[Veiculo] = contexto.get("veiculos", [])
    parametros = contexto.get("parametros")
    distancias_base: Dict[str, float] = contexto.get("metadata", {}).get("distancias_base", {})

    # Ordena entregas por distância à base (crescente)
    entregas_ordenadas = sorted(entregas, key=lambda e: distancias_base.get(e.id, 0.0))

    rotas: List[Rota] = []
    nao_alocadas: List[Entrega] = []

    for veiculo in veiculos:
        peso_atual = 0.0
        volume_atual = 0.0
        paradas: List[ParadaRota] = []
        max_paradas = parametros.max_entregas_por_veiculo if parametros else None

        for entrega in list(entregas_ordenadas):
            if max_paradas and len(paradas) >= max_paradas:
                break
            if peso_atual + entrega.peso_kg > veiculo.capacidade_kg:
                continue
            if volume_atual + entrega.volume_m3 > veiculo.capacidade_m3:
                continue

            seq = len(paradas) + 1
            dist_anterior = 0.0
            if paradas and entrega.endereco.latitude and entrega.endereco.longitude:
                prev = paradas[-1]
                if prev.endereco.latitude and prev.endereco.longitude:
                    dist_anterior = calcular_distancia_km(
                        prev.endereco.latitude,
                        prev.endereco.longitude,
                        entrega.endereco.latitude,
                        entrega.endereco.longitude,
                    )

            paradas.append(
                ParadaRota(
                    sequencia=seq,
                    entrega_id=entrega.id,
                    cliente=entrega.cliente,
                    endereco=entrega.endereco,
                    distancia_anterior_km=round(dist_anterior, 3),
                    tempo_estimado_min=round((dist_anterior / 40) * 60, 1) if dist_anterior else 0.0,
                )
            )
            peso_atual += entrega.peso_kg
            volume_atual += entrega.volume_m3
            entregas_ordenadas.remove(entrega)

        if paradas:
            dist_total = sum(p.distancia_anterior_km for p in paradas)
            tempo_total = sum(p.tempo_estimado_min for p in paradas)
            rotas.append(
                Rota(
                    veiculo_id=veiculo.id,
                    placa=veiculo.placa,
                    paradas=paradas,
                    distancia_total_km=round(dist_total, 3),
                    tempo_total_min=round(tempo_total, 1),
                    peso_total_kg=round(peso_atual, 3),
                    volume_total_m3=round(volume_atual, 4),
                )
            )

    nao_alocadas.extend(entregas_ordenadas)

    contexto["rotas"].extend(rotas)
    contexto["sobras"].extend(nao_alocadas)

    logger.debug(
        "M4: %d rotas criadas, %d entregas não alocadas.",
        len(rotas),
        len(nao_alocadas),
    )
    return contexto
