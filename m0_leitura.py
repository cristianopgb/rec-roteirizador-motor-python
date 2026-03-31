from app.schemas import LogSchema, RoteirizacaoRequestSchema
from app.services.payload_service import carregar_payload_em_dataframes


def executar_m0(payload: RoteirizacaoRequestSchema, logs: list[LogSchema]) -> dict:
    dfs = carregar_payload_em_dataframes(payload)
    ctx = {
        **dfs,
        'parametros': payload.parametros.model_dump(),
    }
    logs.append(LogSchema(modulo='M0', status='ok', mensagem='Leitura do payload concluída', quantidade_entrada=len(payload.carteira), quantidade_saida=len(payload.carteira)))
    return ctx
