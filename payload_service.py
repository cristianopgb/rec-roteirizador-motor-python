import pandas as pd

from app.schemas import RoteirizacaoRequestSchema


def carregar_payload_em_dataframes(payload: RoteirizacaoRequestSchema) -> dict[str, pd.DataFrame]:
    carteira = [item.model_dump(by_alias=True) for item in payload.carteira]
    veiculos = [item.model_dump() for item in payload.veiculos]
    regionalidades = [item.model_dump() for item in payload.regionalidades]

    return {
        'df_carteira_raw': pd.DataFrame(carteira),
        'df_veiculos_raw': pd.DataFrame(veiculos),
        'df_regionalidades_raw': pd.DataFrame(regionalidades),
    }
