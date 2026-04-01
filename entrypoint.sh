#!/usr/bin/env sh
set -e

i=0
until alembic upgrade head; do
  i=$((i + 1))
  if [ "$i" -ge 30 ]; then
    echo "Falha ao aplicar migrações após 30 tentativas."
    exit 1
  fi
  echo "Banco indisponível, aguardando... tentativa $i/30"
  sleep 2
done

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
