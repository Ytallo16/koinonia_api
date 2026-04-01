from __future__ import annotations

from datetime import datetime

from app.models.evento import Evento


def sort_eventos_like_app(eventos: list[Evento], now: datetime | None = None) -> list[Evento]:
    current = now or datetime.now()
    inicio_hoje = datetime(current.year, current.month, current.day, tzinfo=current.tzinfo)

    nao_passados = [e for e in eventos if e.data_hora >= inicio_hoje]
    passados = [e for e in eventos if e.data_hora < inicio_hoje]

    nao_passados.sort(key=lambda e: e.data_hora)
    passados.sort(key=lambda e: e.data_hora, reverse=True)
    return [*nao_passados, *passados]

