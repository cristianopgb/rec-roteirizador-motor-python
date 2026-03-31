# REC Roteirizador - Sistema 2 (Motor Python)

API FastAPI para receber o payload do Sistema 1, validar o contrato e executar o pipeline de roteirização.

## Estrutura

- `app/main.py`: ponto de entrada da API
- `app/api/health.py`: endpoint `/health`
- `app/api/roteirizacao.py`: endpoint `/roteirizar`
- `app/schemas.py`: contrato de request/response
- `app/services/`: validação, pipeline e resposta
- `app/pipeline/`: módulos M0 a M9
- `tests/`: testes básicos

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

### GET /health
Retorna status do serviço.

### POST /roteirizar
Recebe payload com:
- `carteira`
- `veiculos`
- `regionalidades`
- `parametros`

## Próximos passos

1. Integrar o Sistema 1 ao endpoint `/roteirizar`
2. Implementar a lógica real módulo a módulo (M0, M1, M2...)
3. Publicar no Render
