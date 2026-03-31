from app.schemas import LogSchema


def executar_m4(ctx: dict, logs: list[LogSchema]) -> dict:
    ctx['df_manifestos_fechados'] = []
    ctx['df_remanescente_m4'] = ctx['df_roteirizavel']
    logs.append(LogSchema(modulo='M4', status='ok', mensagem='Manifestos fechados executado (stub)', quantidade_entrada=len(ctx['df_roteirizavel']), quantidade_saida=0))
    return ctx
