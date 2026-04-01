from __future__ import annotations

from collections import defaultdict

from sqlalchemy.orm import Session

from app.core.enums import ClassificacaoVocal, StatusFrequencia, TipoPessoa
from app.models.ciclo import Ciclo
from app.models.evento import Evento
from app.models.frequencia import Frequencia
from app.models.pessoa import Pessoa
from app.models.trimestre import Trimestre
from app.schemas.dashboard import DashboardCoralistaItemOut, DashboardNaipeItemOut, DashboardResumoOut


def _build_event_scope_query(db: Session, ano: int | None, trimestre: int | None):
    query = db.query(Evento).join(Trimestre, Evento.trimestre_id == Trimestre.id).join(Ciclo, Trimestre.ciclo_id == Ciclo.id)
    if ano is not None:
        query = query.filter(Ciclo.ano == ano)
    if trimestre is not None:
        query = query.filter(Trimestre.numero == trimestre)
    return query


def _event_ids_in_scope(db: Session, ano: int | None, trimestre: int | None) -> list[str]:
    eventos = _build_event_scope_query(db, ano, trimestre).all()
    return [e.id for e in eventos]


def _voice_label(v: ClassificacaoVocal) -> str:
    return v.value


def _naipe_filter_to_enum(naipe: str | None) -> ClassificacaoVocal | None:
    if naipe is None:
        return None
    normalized = naipe.strip().lower()
    mapping = {
        "soprano": ClassificacaoVocal.soprano,
        "contralto": ClassificacaoVocal.contralto,
        "tenor": ClassificacaoVocal.tenor,
        "baixo": ClassificacaoVocal.baixo,
    }
    return mapping.get(normalized)


def _stats_from_frequencias(freqs: list[Frequencia]) -> tuple[int, int, int, int, int]:
    presenca = sum(1 for f in freqs if f.status in {StatusFrequencia.presenca, StatusFrequencia.atraso})
    falta = sum(1 for f in freqs if f.status == StatusFrequencia.falta)
    fj = sum(1 for f in freqs if f.status == StatusFrequencia.falta_justificada)
    total = presenca + falta + fj
    pct = round((presenca / total) * 100) if total else 0
    return presenca, falta, fj, total, pct


def dashboard_resumo(db: Session, ano: int | None, trimestre: int | None) -> DashboardResumoOut:
    event_ids = _event_ids_in_scope(db, ano, trimestre)

    frequencias_query = db.query(Frequencia)
    if event_ids:
        frequencias_query = frequencias_query.filter(Frequencia.evento_id.in_(event_ids))
    else:
        frequencias_query = frequencias_query.filter(False)
    freqs = frequencias_query.all()

    presencas, faltas, fjs, total, _ = _stats_from_frequencias(freqs)
    coralistas = db.query(Pessoa).filter(Pessoa.tipo_padrao == TipoPessoa.coralista).count()
    eventos = len(event_ids)

    pct_presenca = round((presencas / total) * 100, 2) if total else 0.0
    pct_falta = round((faltas / total) * 100, 2) if total else 0.0
    pct_fj = round((fjs / total) * 100, 2) if total else 0.0

    return DashboardResumoOut(
        coralistas=coralistas,
        eventos=eventos,
        presencas=presencas,
        faltas=faltas,
        faltas_justificadas=fjs,
        percentual_presenca=pct_presenca,
        percentual_falta=pct_falta,
        percentual_falta_justificada=pct_fj,
    )


def dashboard_coralistas(
    db: Session,
    ano: int | None,
    trimestre: int | None,
    naipe: str | None,
) -> list[DashboardCoralistaItemOut]:
    event_ids = _event_ids_in_scope(db, ano, trimestre)
    naipe_enum = _naipe_filter_to_enum(naipe)

    pessoas_query = db.query(Pessoa).filter(Pessoa.tipo_padrao == TipoPessoa.coralista)
    if naipe_enum is not None:
        pessoas_query = pessoas_query.filter(Pessoa.classificacao_vocal == naipe_enum)
    pessoas = pessoas_query.order_by(Pessoa.nome.asc()).all()
    if not pessoas:
        return []

    pessoa_ids = [p.id for p in pessoas]
    freqs_query = db.query(Frequencia).filter(Frequencia.pessoa_id.in_(pessoa_ids))
    if event_ids:
        freqs_query = freqs_query.filter(Frequencia.evento_id.in_(event_ids))
    else:
        freqs_query = freqs_query.filter(False)

    freqs_by_pessoa: dict[str, list[Frequencia]] = defaultdict(list)
    for f in freqs_query.all():
        freqs_by_pessoa[f.pessoa_id].append(f)

    rows: list[DashboardCoralistaItemOut] = []
    for pessoa in pessoas:
        presencas, faltas, fjs, total, pct = _stats_from_frequencias(freqs_by_pessoa.get(pessoa.id, []))
        rows.append(
            DashboardCoralistaItemOut(
                pessoa_id=pessoa.id,
                nome=pessoa.nome,
                classificacao_vocal=_voice_label(pessoa.classificacao_vocal),
                presencas=presencas,
                faltas=faltas,
                faltas_justificadas=fjs,
                total=total,
                percentual_presenca=pct,
            )
        )
    rows.sort(key=lambda x: x.percentual_presenca, reverse=True)
    return rows


def dashboard_naipes(db: Session, ano: int | None, trimestre: int | None) -> list[DashboardNaipeItemOut]:
    all_coralistas = dashboard_coralistas(db, ano, trimestre, naipe=None)
    grouped: dict[str, list[DashboardCoralistaItemOut]] = defaultdict(list)
    for row in all_coralistas:
        grouped[row.classificacao_vocal].append(row)

    output: list[DashboardNaipeItemOut] = []
    for naipe_key in ["soprano", "contralto", "tenor", "baixo"]:
        membros = grouped.get(naipe_key, [])
        presencas = sum(m.presencas for m in membros)
        faltas = sum(m.faltas for m in membros)
        fjs = sum(m.faltas_justificadas for m in membros)
        total = sum(m.total for m in membros)
        pct = round((presencas / total) * 100) if total else 0
        output.append(
            DashboardNaipeItemOut(
                naipe=naipe_key,
                membros=len(membros),
                presencas=presencas,
                faltas=faltas,
                faltas_justificadas=fjs,
                total=total,
                percentual_presenca=pct,
                membros_detalhe=membros,
            )
        )
    return output

