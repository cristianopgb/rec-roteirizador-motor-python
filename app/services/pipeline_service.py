from typing import Any, Dict, List

from app.pipeline.m0_leitura import executar as m0
from app.pipeline.m1_padronizacao import executar as m1
from app.pipeline.m2_enriquecimento import executar as m2
from app.pipeline.m3_triagem import executar as m3
from app.pipeline.m31_fronteira import executar as m31
from app.pipeline.m4_fechados import executar as m4
from app.pipeline.m5_compostos import executar as m5
from app.pipeline.m51_saneamento import executar as m51
from app.pipeline.m8_sobras import executar as m8
from app.pipeline.m9_consolidacao import executar as m9
from app.schemas import RoteirizacaoRequest
from app.utils.logs import get_logger

logger = get_logger(__name__)


def executar_pipeline(request: RoteirizacaoRequest) -> Dict[str, Any]:
    """
    Executa as etapas do pipeline de roteirização em sequência.

    Returns:
        Dicionário com os resultados consolidados do pipeline.
    """
    logger.info("Pipeline iniciado.")

    contexto: Dict[str, Any] = m0(request)
    logger.debug("M0 - leitura concluída.")

    contexto = m1(contexto)
    logger.debug("M1 - padronização concluída.")

    contexto = m2(contexto)
    logger.debug("M2 - enriquecimento concluído.")

    contexto = m3(contexto)
    logger.debug("M3 - triagem concluída.")

    contexto = m31(contexto)
    logger.debug("M3.1 - fronteira concluída.")

    contexto = m4(contexto)
    logger.debug("M4 - fechados concluído.")

    contexto = m5(contexto)
    logger.debug("M5 - compostos concluído.")

    contexto = m51(contexto)
    logger.debug("M5.1 - saneamento concluído.")

    contexto = m8(contexto)
    logger.debug("M8 - sobras concluído.")

    contexto = m9(contexto)
    logger.debug("M9 - consolidação concluída.")

    logger.info("Pipeline finalizado.")
    return contexto
