from app.pipeline.m0_leitura import executar_m0
from app.pipeline.m1_padronizacao import executar_m1
from app.pipeline.m2_enriquecimento import executar_m2
from app.pipeline.m3_triagem import executar_m3
from app.pipeline.m31_fronteira import executar_m31
from app.pipeline.m4_fechados import executar_m4
from app.pipeline.m5_compostos import executar_m5
from app.pipeline.m51_saneamento import executar_m51
from app.pipeline.m8_sobras import executar_m8
from app.pipeline.m9_consolidacao import executar_m9
from app.schemas import LogSchema, RoteirizacaoRequestSchema
from app.services.response_service import montar_resposta_padrao
from app.services.validation_service import validar_payload


def executar_pipeline(payload: RoteirizacaoRequestSchema):
    validar_payload(payload)

    logs: list[LogSchema] = []

    ctx = executar_m0(payload, logs)
    ctx = executar_m1(ctx, logs)
    ctx = executar_m2(ctx, logs)
    ctx = executar_m3(ctx, logs)
    ctx = executar_m31(ctx, logs)
    ctx = executar_m4(ctx, logs)
    ctx = executar_m5(ctx, logs)
    ctx = executar_m51(ctx, logs)
    ctx = executar_m8(ctx, logs)
    ctx = executar_m9(ctx, logs)

    return montar_resposta_padrao(
        total_carteira=len(payload.carteira),
        total_veiculos=len(payload.veiculos),
        total_regionalidades=len(payload.regionalidades),
        logs=logs,
    )
