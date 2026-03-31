"""
Testes básicos da aplicação: health check, pipeline e utilitários.
"""
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.dates import agora_utc, dentro_janela, formatar_data, parse_data
from app.utils.geo import calcular_centro, calcular_distancia_km
from app.utils.numbers import arredondar, percentual, to_float

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "versao" in data
    assert "timestamp" in data


# ---------------------------------------------------------------------------
# Utilitários geográficos
# ---------------------------------------------------------------------------

def test_distancia_km_mesmos_pontos():
    assert calcular_distancia_km(-23.55, -46.63, -23.55, -46.63) == pytest.approx(0.0, abs=1e-6)


def test_distancia_km_entre_cidades():
    # São Paulo → Rio de Janeiro ≈ 357 km
    dist = calcular_distancia_km(-23.5505, -46.6333, -22.9068, -43.1729)
    assert 340 < dist < 380


def test_calcular_centro_lista_vazia():
    lat, lon = calcular_centro([])
    assert lat == 0.0
    assert lon == 0.0


def test_calcular_centro():
    coords = [(-23.0, -46.0), (-24.0, -47.0)]
    lat, lon = calcular_centro(coords)
    assert lat == pytest.approx(-23.5, abs=0.01)
    assert lon == pytest.approx(-46.5, abs=0.01)


# ---------------------------------------------------------------------------
# Utilitários numéricos
# ---------------------------------------------------------------------------

def test_arredondar():
    assert arredondar(3.14159, 2) == 3.14


def test_to_float_valido():
    assert to_float("3.5") == 3.5


def test_to_float_invalido():
    assert to_float("abc") == 0.0
    assert to_float(None) == 0.0


def test_percentual():
    assert percentual(1, 4) == 25.0
    assert percentual(0, 0) == 0.0


# ---------------------------------------------------------------------------
# Utilitários de datas
# ---------------------------------------------------------------------------

def test_agora_utc():
    now = agora_utc()
    assert now.tzinfo is not None


def test_formatar_data():
    dt = datetime(2024, 6, 15, 10, 30, 0)
    assert formatar_data(dt) == "15/06/2024 10:30:00"


def test_parse_data_valido():
    resultado = parse_data("2024-06-15T10:30:00")
    assert resultado is not None
    assert resultado.year == 2024


def test_parse_data_invalido():
    resultado = parse_data("not-a-date")
    assert resultado is None


def test_dentro_janela_sem_restricao():
    dt = datetime(2024, 6, 15, 10, 0, 0)
    assert dentro_janela(dt, None, None) is True


def test_dentro_janela_fora():
    dt = datetime(2024, 6, 15, 10, 0, 0)
    inicio = datetime(2024, 6, 15, 11, 0, 0)
    assert dentro_janela(dt, inicio, None) is False


# ---------------------------------------------------------------------------
# Endpoint de roteirização
# ---------------------------------------------------------------------------

PAYLOAD_VALIDO = {
    "entregas": [
        {
            "id": "e1",
            "cliente": "Cliente A",
            "endereco": {
                "logradouro": "Rua das Flores",
                "cidade": "São Paulo",
                "estado": "SP",
                "latitude": -23.56,
                "longitude": -46.64,
            },
            "peso_kg": 10.0,
            "volume_m3": 0.05,
        }
    ],
    "veiculos": [
        {
            "id": "v1",
            "placa": "ABC1234",
            "capacidade_kg": 1000.0,
            "capacidade_m3": 5.0,
            "base_latitude": -23.55,
            "base_longitude": -46.63,
        }
    ],
    "parametros": {
        "data_roteirizacao": "2024-06-15T08:00:00",
        "retornar_base": True,
        "otimizar_por": "distancia",
    },
}


def test_roteirizacao_sucesso():
    response = client.post("/api/v1/roteirizacao", json=PAYLOAD_VALIDO)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sucesso"
    assert "rotas" in data
    assert "estatisticas" in data


def test_roteirizacao_sem_entregas():
    payload = {**PAYLOAD_VALIDO, "entregas": []}
    response = client.post("/api/v1/roteirizacao", json=payload)
    assert response.status_code == 422


def test_roteirizacao_sem_veiculos():
    payload = {**PAYLOAD_VALIDO, "veiculos": []}
    response = client.post("/api/v1/roteirizacao", json=payload)
    assert response.status_code == 422
