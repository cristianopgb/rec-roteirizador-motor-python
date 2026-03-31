from app.schemas import LogSchema, ResumoSchema, RoteirizacaoResponseSchema


def montar_resposta_padrao(total_carteira: int, total_veiculos: int, total_regionalidades: int, logs: list[LogSchema]) -> RoteirizacaoResponseSchema:
    return RoteirizacaoResponseSchema(
        status='sucesso',
        mensagem='Payload recebido e validado com sucesso',
        resumo=ResumoSchema(
            total_carteira=total_carteira,
            total_veiculos=total_veiculos,
            total_regionalidades=total_regionalidades,
        ),
        manifestos_fechados=[],
        manifestos_compostos=[],
        nao_roteirizados=[],
        logs=logs,
    )
