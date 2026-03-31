from app.schemas import LogSchema


def executar_m1(ctx: dict, logs: list[LogSchema]) -> dict:
    # TODO: padronização real de tipos e nomes internos
    logs.append(LogSchema(modulo='M1', status='ok', mensagem='Padronização executada (stub)', quantidade_entrada=len(ctx['df_carteira_raw']), quantidade_saida=len(ctx['df_carteira_raw'])))
    ctx['df_carteira_tratada'] = ctx['df_carteira_raw'].copy()
    ctx['df_veiculos_tratados'] = ctx['df_veiculos_raw'].copy()
    ctx['df_regionalidades_tratadas'] = ctx['df_regionalidades_raw'].copy()
    return ctx
