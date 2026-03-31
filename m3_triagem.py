from app.schemas import LogSchema


def executar_m3(ctx: dict, logs: list[LogSchema]) -> dict:
    df = ctx['df_carteira_enriquecida'].copy()
    ctx['df_roteirizavel'] = df.copy()
    ctx['df_entrega_futura'] = df.iloc[0:0].copy()
    ctx['df_aguardando_agendamento'] = df.iloc[0:0].copy()
    ctx['df_excecoes'] = df.iloc[0:0].copy()
    logs.append(LogSchema(modulo='M3', status='ok', mensagem='Triagem executada (stub)', quantidade_entrada=len(df), quantidade_saida=len(ctx['df_roteirizavel'])))
    return ctx
