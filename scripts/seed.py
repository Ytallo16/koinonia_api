from __future__ import annotations

from datetime import date, datetime

from app.core.enums import (
    ClassificacaoVocal,
    FuncaoTrimestre,
    Naipe,
    StatusFrequencia,
    TipoPessoa,
)
from app.core.database import SessionLocal
from app.models.ciclo import Ciclo
from app.models.evento import Evento
from app.models.frequencia import Frequencia
from app.models.matricula import Matricula
from app.models.musica_escala import MusicaEscala
from app.models.musica_evento import MusicaEvento
from app.models.pessoa import Pessoa
from app.models.trimestre import Trimestre


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Pessoa).count() > 0:
            print("Seed ignorado: já existem dados em pessoas.")
            return

        pessoas = [
            Pessoa(
                nome="João Silva",
                data_nascimento=date(1990, 1, 1),
                telefone="(11) 99999-0001",
                classificacao_vocal=ClassificacaoVocal.tenor,
                tipo_padrao=TipoPessoa.coralista,
            ),
            Pessoa(
                nome="Maria Santos",
                data_nascimento=date(1985, 5, 10),
                telefone="(11) 99999-0002",
                classificacao_vocal=ClassificacaoVocal.soprano,
                tipo_padrao=TipoPessoa.coralista,
            ),
            Pessoa(
                nome="Pedro Oliveira",
                data_nascimento=date(1975, 12, 15),
                telefone="(11) 99999-0003",
                classificacao_vocal=ClassificacaoVocal.baixo,
                tipo_padrao=TipoPessoa.regente,
            ),
            Pessoa(
                nome="Ana Costa",
                data_nascimento=date(1992, 3, 22),
                telefone="(11) 99999-0004",
                classificacao_vocal=ClassificacaoVocal.contralto,
                tipo_padrao=TipoPessoa.coralista,
            ),
        ]
        db.add_all(pessoas)
        db.flush()

        ciclo = Ciclo(ano=2026, ativo=True)
        db.add(ciclo)
        db.flush()

        trimestres = []
        for n in [1, 2, 3, 4]:
            t = Trimestre(ciclo_id=ciclo.id, numero=n)
            trimestres.append(t)
            db.add(t)
        db.flush()

        t1 = trimestres[0]
        for p in pessoas:
            funcao = FuncaoTrimestre.regente if p.tipo_padrao == TipoPessoa.regente else FuncaoTrimestre.coralista
            db.add(Matricula(trimestre_id=t1.id, pessoa_id=p.id, funcao_no_trimestre=funcao))

        e1 = Evento(
            trimestre_id=t1.id,
            data_hora=datetime(2026, 2, 20, 19, 0),
            nome="Ensaio Geral - Fevereiro",
            descricao="Ensaio geral com foco no repertório de fevereiro.",
        )
        e2 = Evento(
            trimestre_id=t1.id,
            data_hora=datetime(2026, 2, 27, 19, 0),
            nome="Ensaio de Naipe - Soprano",
            descricao="Ajustes de afinação e dinâmica para o naipe soprano.",
        )
        db.add_all([e1, e2])
        db.flush()

        m1 = MusicaEvento(evento_id=e1.id, nome="Grande é o Senhor", link="https://example.com/grande", ordem=1)
        m2 = MusicaEvento(evento_id=e1.id, nome="Aleluia", link="https://example.com/aleluia", ordem=2)
        db.add_all([m1, m2])
        db.flush()

        by_name = {p.nome: p.id for p in pessoas}
        db.add_all(
            [
                MusicaEscala(musica_id=m1.id, naipe=Naipe.soprano, pessoa_id=by_name.get("Maria Santos")),
                MusicaEscala(musica_id=m1.id, naipe=Naipe.contralto, pessoa_id=by_name.get("Ana Costa")),
                MusicaEscala(musica_id=m1.id, naipe=Naipe.tenor, pessoa_id=by_name.get("João Silva")),
                MusicaEscala(musica_id=m2.id, naipe=Naipe.soprano, pessoa_id=by_name.get("Maria Santos")),
            ]
        )

        db.add_all(
            [
                Frequencia(evento_id=e1.id, pessoa_id=by_name["João Silva"], status=StatusFrequencia.presenca),
                Frequencia(evento_id=e1.id, pessoa_id=by_name["Maria Santos"], status=StatusFrequencia.falta),
                Frequencia(evento_id=e1.id, pessoa_id=by_name["Ana Costa"], status=StatusFrequencia.presenca),
                Frequencia(
                    evento_id=e2.id,
                    pessoa_id=by_name["Maria Santos"],
                    status=StatusFrequencia.falta_justificada,
                    justificativa="Consulta médica",
                ),
            ]
        )
        db.commit()
        print("Seed concluído.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
