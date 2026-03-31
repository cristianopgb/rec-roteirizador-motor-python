from fastapi import APIRouter

from app.schemas import RoteirizacaoRequestSchema, RoteirizacaoResponseSchema
from app.services.pipeline_service import executar_pipeline

router = APIRouter(tags=['roteirizacao'])


@router.post('/roteirizar', response_model=RoteirizacaoResponseSchema)
def roteirizar(payload: RoteirizacaoRequestSchema):
    return executar_pipeline(payload)
