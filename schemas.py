from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CarteiraItemSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    filial: Any = Field(alias='Filial')
    romane: Any = Field(alias='Romane')
    filial_origem: Any = Field(alias='Filial (origem)')
    serie: Any = Field(alias='Série')
    nro_doc: Any = Field(alias='Nro Doc.')
    data_des: Any = Field(alias='Data Des')
    data_nf: Any = Field(alias='Data NF')
    dle: Any = Field(alias='D.L.E.')
    agendam: Any = Field(alias='Agendam.')
    palet: Any = Field(alias='Palet')
    conf: Any = Field(alias='Conf')
    peso: Any = Field(alias='Peso')
    vlr_merc: Any = Field(alias='Vlr.Merc.')
    qtd: Any = Field(alias='Qtd.')
    peso_c: Any = Field(alias='Peso C')
    classifi: Any = Field(alias='Classifi')
    tomador: Any = Field(alias='Tomador')
    destinatario: Any = Field(alias='Destinatário')
    bairro: Any = Field(alias='Bairro')
    cida: Any = Field(alias='Cida')
    uf: Any = Field(alias='UF')
    nf_serie: Any = Field(alias='NF / Serie')
    tipo_carga: Any = Field(alias='Tipo Carga')
    qtd_nf: Any = Field(alias='Qtd.NF')
    regiao: Any = Field(alias='Região')
    sub_regiao: Any = Field(alias='Sub-Região')
    ocorrencias_nfs: Any = Field(alias='Ocorrências NFs')
    remetente: Any = Field(alias='Remetente')
    observacao_r: Any = Field(alias='Observação R')
    ref_cliente: Any = Field(alias='Ref Cliente')
    cidade_dest: Any = Field(alias='Cidade Dest.')
    mesoregiao: Any = Field(alias='Mesoregião')
    agenda: Any = Field(alias='Agenda')
    tipo_c: Any = Field(alias='Tipo C')
    ultima: Any = Field(alias='Última')
    status: Any = Field(alias='Status')
    lat: Any = Field(alias='Lat.')
    lon: Any = Field(alias='Lon.')


class VeiculoSchema(BaseModel):
    id: Any
    placa: Any
    perfil: Any
    tipo_veiculo: Any
    capacidade_peso_kg: Any
    capacidade_vol_m3: Any
    qtd_eixos: Any
    max_entregas: Any
    max_km_distancia: Any
    ocupacao_minima_perc: Any
    dedicado: Any
    tipo_frota: Any
    filial_id: Any
    ativo: Any


class RegionalidadeSchema(BaseModel):
    cidade: Any
    uf: Any
    mesorregiao: Any
    microrregiao: Any


class ParametrosSchema(BaseModel):
    usuario_id: Any | None = None
    usuario_nome: Any | None = None
    filial_id: Any | None = None
    filial_nome: Any | None = None
    data_execucao: Any
    modelo_roteirizacao: Any | None = None
    filtros_aplicados: dict[str, Any] | None = None
    origem_sistema: Any | None = None


class RoteirizacaoRequestSchema(BaseModel):
    carteira: list[CarteiraItemSchema]
    veiculos: list[VeiculoSchema]
    regionalidades: list[RegionalidadeSchema]
    parametros: ParametrosSchema


class ResumoSchema(BaseModel):
    total_carteira: int = 0
    total_veiculos: int = 0
    total_regionalidades: int = 0
    total_roteirizado: int = 0
    total_nao_roteirizado: int = 0
    total_manifestos_fechados: int = 0
    total_manifestos_compostos: int = 0
    ocupacao_media_peso: float = 0.0
    ocupacao_media_volume: float = 0.0


class LogSchema(BaseModel):
    modulo: str
    status: Literal['ok', 'erro']
    mensagem: str
    quantidade_entrada: int = 0
    quantidade_saida: int = 0


class RoteirizacaoResponseSchema(BaseModel):
    status: Literal['sucesso', 'erro']
    mensagem: str
    resumo: ResumoSchema
    manifestos_fechados: list[dict[str, Any]]
    manifestos_compostos: list[dict[str, Any]]
    nao_roteirizados: list[dict[str, Any]]
    logs: list[LogSchema]
