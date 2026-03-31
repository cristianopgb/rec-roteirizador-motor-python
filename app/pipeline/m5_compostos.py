"""
M5 - Compostos
Cria rotas compostas combinando entregas de regiões próximas que não foram
alocadas nas rotas fechadas, otimizando o uso residual da frota.
"""
from typing import Any, Dict, List

from app.schemas import Entrega, ParadaRota, Rota, Veiculo
from app.utils.geo import calcular_distancia_km
from app.utils.logs import get_logger

logger = get_logger(__name__)

RAIO_COMPOSICAO_KM = 10.0


def executar(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agrupa sobras por proximidade geográfica e tenta alocar nos veículos
    que ainda possuem capacidade residual.

    Args:
        contexto: Contexto atual do pipeline.

    Returns:
        Contexto atualizado.
    """
    sobras_entrada: List[Entrega] = list(contexto.get("sobras", []))
    veiculos: List[Veiculo] = contexto.get("veiculos", [])
    rotas_existentes: List[Rota] = contexto.get("rotas", [])

    if not sobras_entrada or not veiculos:
        return contexto

    # Calcula capacidade residual por veículo
    capacidade_residual: Dict[str, Dict[str, float]] = {}
    for veiculo in veiculos:
        peso_usado = sum(r.peso_total_kg for r in rotas_existentes if r.veiculo_id == veiculo.id)
        vol_usado = sum(r.volume_total_m3 for r in rotas_existentes if r.veiculo_id == veiculo.id)
        capacidade_residual[veiculo.id] = {
            "peso": veiculo.capacidade_kg - peso_usado,
            "volume": veiculo.capacidade_m3 - vol_usado,
            "veiculo": veiculo,
        }

    novas_sobras: List[Entrega] = []
    novas_rotas: List[Rota] = []

    # Agrupa por célula geográfica (grau inteiro de lat/lon)
    clusters: Dict[str, List[Entrega]] = {}
    for entrega in sobras_entrada:
        if entrega.endereco.latitude is None or entrega.endereco.longitude is None:
            novas_sobras.append(entrega)
            continue
        chave = f"{int(entrega.endereco.latitude)},{int(entrega.endereco.longitude)}"
        clusters.setdefault(chave, []).append(entrega)

    for chave, grupo in clusters.items():
        for veiculo_id, cap in capacidade_residual.items():
            if not grupo:
                break
            paradas: List[ParadaRota] = []
            peso_atual = 0.0
            vol_atual = 0.0
            alocadas: List[Entrega] = []

            for entrega in list(grupo):
                if peso_atual + entrega.peso_kg > cap["peso"]:
                    continue
                if vol_atual + entrega.volume_m3 > cap["volume"]:
                    continue
                paradas.append(
                    ParadaRota(
                        sequencia=len(paradas) + 1,
                        entrega_id=entrega.id,
                        cliente=entrega.cliente,
                        endereco=entrega.endereco,
                    )
                )
                peso_atual += entrega.peso_kg
                vol_atual += entrega.volume_m3
                alocadas.append(entrega)
                grupo.remove(entrega)

            if paradas:
                veiculo_obj: Veiculo = cap["veiculo"]
                dist_total = sum(p.distancia_anterior_km for p in paradas)
                novas_rotas.append(
                    Rota(
                        veiculo_id=veiculo_obj.id,
                        placa=veiculo_obj.placa,
                        paradas=paradas,
                        distancia_total_km=round(dist_total, 3),
                        tempo_total_min=0.0,
                        peso_total_kg=round(peso_atual, 3),
                        volume_total_m3=round(vol_atual, 4),
                    )
                )
                cap["peso"] -= peso_atual
                cap["volume"] -= vol_atual

            novas_sobras.extend(grupo)

    contexto["rotas"].extend(novas_rotas)
    contexto["sobras"] = novas_sobras

    logger.debug(
        "M5: %d rotas compostas criadas, %d sobras restantes.",
        len(novas_rotas),
        len(novas_sobras),
    )
    return contexto
