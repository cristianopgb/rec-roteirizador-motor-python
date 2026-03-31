from app.schemas import RoteirizacaoRequestSchema


REQUIRED_BLOCKS = ['carteira', 'veiculos', 'regionalidades', 'parametros']


def validar_payload(payload: RoteirizacaoRequestSchema) -> None:
    # Pydantic já valida a estrutura principal; este ponto fica reservado para regras adicionais.
    if payload.carteira is None or payload.veiculos is None or payload.regionalidades is None or payload.parametros is None:
        raise ValueError('Payload inválido: blocos obrigatórios ausentes.')
