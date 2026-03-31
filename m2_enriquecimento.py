from app.schemas import LogSchema


def executar_m2(ctx: dict, logs: list[LogSchema]) -> dict:
    # TODO: enriquecimento geográfico e temporal real
    logs.append(LogSchema(modulo='M2', status='ok', mensagem='Enriquecimento executado (stub)', quantidade_entrada=len(ctx['df_carteira_tratada']), quantidade_saida=len(ctx['df_carteira_tratada'])))
    ctx['df_carteira_enriquecida'] = ctx['df_carteira_tratada'].copy()
    return ctx
