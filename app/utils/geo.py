"""
utils/geo.py
Utilitários geográficos: cálculo de distâncias e conversões.
"""
import math
from typing import Tuple

RAIO_TERRA_KM = 6371.0


def calcular_distancia_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância em linha reta (Haversine) entre dois pontos geográficos.

    Args:
        lat1: Latitude do ponto 1 em graus decimais.
        lon1: Longitude do ponto 1 em graus decimais.
        lat2: Latitude do ponto 2 em graus decimais.
        lon2: Longitude do ponto 2 em graus decimais.

    Returns:
        Distância em quilômetros.
    """
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RAIO_TERRA_KM * c


def calcular_centro(coordenadas: list) -> Tuple[float, float]:
    """
    Calcula o centróide de uma lista de coordenadas (lat, lon).

    Args:
        coordenadas: Lista de tuplas (latitude, longitude).

    Returns:
        Tupla (latitude_media, longitude_media) ou (0.0, 0.0) se vazia.
    """
    if not coordenadas:
        return 0.0, 0.0
    lat_media = sum(c[0] for c in coordenadas) / len(coordenadas)
    lon_media = sum(c[1] for c in coordenadas) / len(coordenadas)
    return round(lat_media, 6), round(lon_media, 6)


def graus_para_radianos(graus: float) -> float:
    """Converte graus decimais para radianos."""
    return math.radians(graus)
