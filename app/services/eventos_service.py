from __future__ import annotations

from datetime import datetime

from app.models.evento import Evento


def _to_local_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone().replace(tzinfo=None)


def sort_eventos_like_app(eventos: list[Evento], now: datetime | None = None) -> list[Evento]:
    current = _to_local_naive(now or datetime.now())
    inicio_hoje = datetime(current.year, current.month, current.day)

    nao_passados = [e for e in eventos if _to_local_naive(e.data_hora) >= inicio_hoje]
    passados = [e for e in eventos if _to_local_naive(e.data_hora) < inicio_hoje]

    nao_passados.sort(key=lambda e: _to_local_naive(e.data_hora))
    passados.sort(key=lambda e: _to_local_naive(e.data_hora), reverse=True)
    return [*nao_passados, *passados]
