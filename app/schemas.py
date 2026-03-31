from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Modelos de entrada
# ---------------------------------------------------------------------------

class Endereco(BaseModel):
    logradouro: str
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: str
    estado: str
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Entrega(BaseModel):
    id: str
    cliente: str
    endereco: Endereco
    peso_kg: float = Field(ge=0)
    volume_m3: float = Field(ge=0)
    janela_inicio: Optional[datetime] = None
    janela_fim: Optional[datetime] = None
    prioridade: int = Field(default=1, ge=1, le=5)
    observacoes: Optional[str] = None


class Veiculo(BaseModel):
    id: str
    placa: str
    capacidade_kg: float = Field(ge=0)
    capacidade_m3: float = Field(ge=0)
    base_latitude: float
    base_longitude: float
    disponivel: bool = True


class ParametrosRoteirizacao(BaseModel):
    data_roteirizacao: datetime
    retornar_base: bool = True
    otimizar_por: str = Field(default="distancia", pattern="^(distancia|tempo|custo)$")
    max_entregas_por_veiculo: Optional[int] = Field(default=None, ge=1)
    raio_max_km: Optional[float] = Field(default=None, ge=0)


class RoteirizacaoRequest(BaseModel):
    entregas: List[Entrega]
    veiculos: List[Veiculo]
    parametros: ParametrosRoteirizacao


# ---------------------------------------------------------------------------
# Modelos de saída
# ---------------------------------------------------------------------------

class ParadaRota(BaseModel):
    sequencia: int
    entrega_id: str
    cliente: str
    endereco: Endereco
    distancia_anterior_km: float = 0.0
    tempo_estimado_min: float = 0.0


class Rota(BaseModel):
    veiculo_id: str
    placa: str
    paradas: List[ParadaRota]
    distancia_total_km: float = 0.0
    tempo_total_min: float = 0.0
    peso_total_kg: float = 0.0
    volume_total_m3: float = 0.0


class EstatisticasRoteirizacao(BaseModel):
    total_entregas: int
    entregas_roteirizadas: int
    entregas_nao_roteirizadas: int
    total_rotas: int
    distancia_total_km: float
    tempo_total_min: float


class RoteirizacaoResponse(BaseModel):
    status: str
    mensagem: str
    rotas: List[Rota] = []
    sobras: List[Entrega] = []
    estatisticas: Optional[EstatisticasRoteirizacao] = None
    metadata: Dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str
    versao: str
    timestamp: datetime
