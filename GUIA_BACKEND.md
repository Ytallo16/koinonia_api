# Backend FastAPI - Frequência Koinonia

## 1) Visão de arquitetura
- Stack: FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL.
- Sem autenticação (v1).
- Subida local: Docker Compose (`api` + `db`).
- Upload de anexos em volume dedicado (`/app/uploads`).

Fluxo de camadas:
1. `routers` recebem HTTP e validam entrada/saída.
2. `repositories` executam operações de persistência.
3. `services` aplicam regras de negócio (ativação de ciclo, ordenação de eventos, dashboards, início).
4. `models` representam o esquema relacional.
5. `schemas` definem contratos públicos da API.

## 2) Diagrama textual: telas -> endpoints
- Início (`InicioScreen`)
1. `GET /inicio/resumo`

- Eventos por trimestre (`HomeScreen` + `CalendarioEnsaiosScreen`)
1. `GET /ciclos`
2. `GET /ciclos/{ciclo_id}/trimestres`
3. `GET /trimestres/{trimestre_id}/eventos`
4. `POST /eventos`
5. `GET /eventos/{evento_id}`
6. `PUT /eventos/{evento_id}`
7. `DELETE /eventos/{evento_id}`
8. `POST /eventos/{evento_id}/anexo`
9. `GET /eventos/{evento_id}/anexo`
10. `DELETE /eventos/{evento_id}/anexo`

- Chamada interativa (`ChamadaInterativaScreen`)
1. `GET /trimestres/{trimestre_id}/matriculas`
2. `PUT /trimestres/{trimestre_id}/matriculas`
3. `GET /eventos/{evento_id}/frequencias`
4. `PUT /eventos/{evento_id}/frequencias`
5. `PATCH /frequencias/{frequencia_id}`

- Detalhes do evento (músicas/escalas)
1. `GET /eventos/{evento_id}/musicas`
2. `POST /eventos/{evento_id}/musicas`
3. `PUT /eventos/{evento_id}/musicas/{musica_id}`
4. `DELETE /eventos/{evento_id}/musicas/{musica_id}`
5. `PUT /musicas/{musica_id}/escalas`

- Coralistas
1. `GET /pessoas`
2. `POST /pessoas`
3. `PUT /pessoas/{pessoa_id}`
4. `DELETE /pessoas/{pessoa_id}`

- Estatísticas
1. `GET /dashboard/resumo?ano=&trimestre=`
2. `GET /dashboard/coralistas?ano=&trimestre=&naipe=`
3. `GET /dashboard/naipes?ano=&trimestre=`

## 3) Execução com Docker (passo a passo)
Dentro da pasta `backend/`:

```bash
cp .env.example .env
docker compose up --build -d
```

Após subir:
- Docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

Parar:

```bash
docker compose down
```

## 4) Migrações e seed inicial
- O container da API executa `alembic upgrade head` no startup (`entrypoint.sh`).
- Seed opcional:

```bash
docker compose exec api python scripts/seed.py
```

## 5) Catálogo de endpoints (contrato v1)
- Saúde
1. `GET /health`

- Pessoas
1. `GET /pessoas`
2. `POST /pessoas`
3. `PUT /pessoas/{pessoa_id}`
4. `DELETE /pessoas/{pessoa_id}`

- Ciclos e trimestres
1. `GET /ciclos`
2. `POST /ciclos`
3. `PATCH /ciclos/{ciclo_id}/ativar`
4. `GET /ciclos/{ciclo_id}/trimestres`
5. `POST /trimestres`

- Matrículas trimestrais
1. `GET /trimestres/{trimestre_id}/matriculas`
2. `PUT /trimestres/{trimestre_id}/matriculas`

- Eventos
1. `GET /trimestres/{trimestre_id}/eventos`
2. `POST /eventos`
3. `GET /eventos/{evento_id}`
4. `PUT /eventos/{evento_id}`
5. `DELETE /eventos/{evento_id}`

- Anexo de evento
1. `POST /eventos/{evento_id}/anexo` (multipart/form-data)
2. `GET /eventos/{evento_id}/anexo`
3. `DELETE /eventos/{evento_id}/anexo`

- Músicas e escalas
1. `GET /eventos/{evento_id}/musicas`
2. `POST /eventos/{evento_id}/musicas`
3. `PUT /eventos/{evento_id}/musicas/{musica_id}`
4. `DELETE /eventos/{evento_id}/musicas/{musica_id}`
5. `PUT /musicas/{musica_id}/escalas`

- Frequências
1. `GET /eventos/{evento_id}/frequencias`
2. `PUT /eventos/{evento_id}/frequencias`
3. `PATCH /frequencias/{frequencia_id}`

- Dashboards
1. `GET /dashboard/resumo`
2. `GET /dashboard/coralistas`
3. `GET /dashboard/naipes`
4. `GET /inicio/resumo`

## 6) Exemplos curl
Criar pessoa:

```bash
curl -X POST http://localhost:8000/pessoas \
  -H "Content-Type: application/json" \
  -d '{
    "nome":"Maria Santos",
    "data_nascimento":"1985-05-10",
    "telefone":"(11) 99999-0002",
    "classificacao_vocal":"soprano",
    "tipo_padrao":"coralista"
  }'
```

Criar ciclo com 4 trimestres:

```bash
curl -X POST http://localhost:8000/ciclos \
  -H "Content-Type: application/json" \
  -d '{"ano":2026,"ativo":true,"criar_trimestres":true}'
```

Criar evento:

```bash
curl -X POST http://localhost:8000/eventos \
  -H "Content-Type: application/json" \
  -d '{
    "trimestre_id":"TRIMESTRE_ID",
    "nome":"Ensaio Geral",
    "descricao":"Repertório de abril",
    "data_hora":"2026-04-03T19:30:00"
  }'
```

Salvar chamada em lote:

```bash
curl -X PUT http://localhost:8000/eventos/EVENTO_ID/frequencias \
  -H "Content-Type: application/json" \
  -d '{
    "frequencias":[
      {"pessoa_id":"P1","status":"presenca"},
      {"pessoa_id":"P2","status":"falta_justificada","justificativa":"Consulta médica"}
    ]
  }'
```

Upload de anexo:

```bash
curl -X POST http://localhost:8000/eventos/EVENTO_ID/anexo \
  -F "file=@/caminho/arquivo.pdf"
```

## 7) Checklist de integração Flutter (trocar mock_data)
1. Criar camada `ApiClient` no Flutter (Dio/http) com base URL do backend.
2. Substituir leituras de `mockPessoas`, `mockEventos`, `mockFrequencias`, `mockMatriculas`, `mockCiclos`, `mockTrimestres` por chamadas REST.
3. `InicioScreen`:
   - trocar cálculos locais por `GET /inicio/resumo`.
4. `HomeScreen`:
   - `GET /ciclos` + `GET /ciclos/{id}/trimestres`.
5. `CalendarioEnsaiosScreen`:
   - `GET /trimestres/{id}/eventos`, `POST /eventos`, `PUT /eventos/{id}`.
6. `ChamadaInterativaScreen`:
   - carregar `GET /trimestres/{id}/matriculas` + `GET /eventos/{id}/frequencias`;
   - salvar via `PUT /eventos/{id}/frequencias`.
7. `CoralistasScreen`:
   - CRUD via `/pessoas`.
8. `EventoDetalhesScreen`:
   - músicas/escalas e anexos usando endpoints dedicados.
9. `EstatisticasScreen`:
   - usar `/dashboard/resumo`, `/dashboard/coralistas`, `/dashboard/naipes`.

## 8) Troubleshooting
- API não sobe por migração:
1. Verifique logs: `docker compose logs api`.
2. Garanta credenciais do Postgres no `.env`.

- Erro de conexão com banco:
1. Confirme `db` ativo: `docker compose ps`.
2. Confirme `DATABASE_URL` usando host `db` (dentro do compose).

- Upload não funciona:
1. Verifique volume `uploads_data`.
2. Verifique permissão da pasta `UPLOAD_DIR`.

- CORS no Flutter Web:
1. Ajuste `CORS_ORIGINS` no `.env`.
2. Reinicie containers (`docker compose up -d --build`).

- Dados não aparecem no app:
1. Confirme base URL correta no Flutter.
2. Teste endpoint no browser/curl.
3. Rode seed inicial para dados de demonstração.
