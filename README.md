# rec-roteirizador-motor-python

Motor de cálculo de roteirização para logística, desenvolvido em Python com FastAPI.

## Estrutura do Projeto

```
├── app/
│   ├── main.py              # Entrypoint FastAPI
│   ├── schemas.py           # Modelos Pydantic (request/response)
│   ├── config.py            # Configurações da aplicação
│   ├── api/
│   │   ├── health.py        # Endpoint de health check
│   │   └── roteirizacao.py  # Endpoint de roteirização
│   ├── services/
│   │   ├── validation_service.py  # Validação da requisição
│   │   ├── pipeline_service.py    # Orquestração do pipeline
│   │   └── response_service.py    # Construção da resposta
│   ├── pipeline/
│   │   ├── m0_leitura.py          # Leitura e inicialização do contexto
│   │   ├── m1_padronizacao.py     # Padronização dos dados
│   │   ├── m2_enriquecimento.py   # Enriquecimento (geocodificação)
│   │   ├── m3_triagem.py          # Triagem e classificação
│   │   ├── m31_fronteira.py       # Tratamento de entregas de fronteira
│   │   ├── m4_fechados.py         # Montagem de rotas fechadas
│   │   ├── m5_compostos.py        # Rotas compostas (sobras)
│   │   ├── m51_saneamento.py      # Saneamento das rotas
│   │   ├── m8_sobras.py           # Diagnóstico de não-alocados
│   │   └── m9_consolidacao.py     # Consolidação e totais
│   └── utils/
│       ├── dates.py         # Utilitários de data/hora
│       ├── numbers.py       # Utilitários numéricos
│       ├── geo.py           # Utilitários geográficos (Haversine)
│       └── logs.py          # Configuração de logging
├── tests/
│   └── test_app.py          # Testes da aplicação
├── requirements.txt
├── Dockerfile
├── render.yaml
└── README.md
```

## Como Executar

### Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse a documentação em: http://localhost:8000/docs

### Docker

```bash
docker build -t roteirizador .
docker run -p 8000:8000 roteirizador
```

## Testes

```bash
pytest tests/
```

## Endpoints

| Método | Rota                    | Descrição               |
|--------|-------------------------|-------------------------|
| GET    | `/api/v1/health`        | Health check            |
| POST   | `/api/v1/roteirizacao`  | Executa roteirização    |
