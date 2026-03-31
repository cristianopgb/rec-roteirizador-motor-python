from app.schemas import LogSchema


def executar_m8(ctx: dict, logs: list[LogSchema]) -> dict:
    ctx['df_nao_roteirizados'] = []
    logs.append(LogSchema(modulo='M8', status='ok', mensagem='Classificação de sobras executada (stub)', quantidade_entrada=len(ctx['df_remanescente_m5']), quantidade_saida=0))
    return ctx
