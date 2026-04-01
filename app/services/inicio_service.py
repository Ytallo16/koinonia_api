from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.enums import TipoPessoa
from app.models.ciclo import Ciclo
from app.models.evento import Evento
from app.models.musica_evento import MusicaEvento
from app.models.pessoa import Pessoa
from app.schemas.inicio import InicioResumoOut, ProximoEventoOut


def inicio_resumo(db: Session, now: datetime | None = None) -> InicioResumoOut:
    reference = now or datetime.now()
    inicio_semana = reference
    fim_semana = reference + timedelta(days=7)

    total_coralistas = db.query(Pessoa).filter(Pessoa.tipo_padrao == TipoPessoa.coralista).count()
    total_musicas = db.query(MusicaEvento).count()
    total_eventos = db.query(Evento).count()

    eventos_mes = (
        db.query(Evento)
        .filter(Evento.data_hora >= datetime(reference.year, reference.month, 1, tzinfo=reference.tzinfo))
        .filter(
            Evento.data_hora
            < (
                datetime(reference.year + 1, 1, 1, tzinfo=reference.tzinfo)
                if reference.month == 12
                else datetime(reference.year, reference.month + 1, 1, tzinfo=reference.tzinfo)
            )
        )
        .count()
    )
    eventos_semana = (
        db.query(Evento)
        .filter(Evento.data_hora >= inicio_semana)
        .filter(Evento.data_hora < fim_semana)
        .count()
    )

    proximo = (
        db.query(Evento)
        .filter(Evento.data_hora >= reference)
        .order_by(Evento.data_hora.asc())
        .first()
    )
    ciclo_ativo = db.query(Ciclo).filter(Ciclo.ativo.is_(True)).first()

    return InicioResumoOut(
        ano_ativo=ciclo_ativo.ano if ciclo_ativo else None,
        total_coralistas=total_coralistas,
        total_musicas=total_musicas,
        total_eventos=total_eventos,
        eventos_no_mes=eventos_mes,
        eventos_na_semana=eventos_semana,
        proximo_evento=(
            ProximoEventoOut(
                id=proximo.id,
                nome=proximo.nome,
                data_hora=proximo.data_hora,
                trimestre_id=proximo.trimestre_id,
            )
            if proximo
            else None
        ),
    )

