from enum import Enum


class ClassificacaoVocal(str, Enum):
    soprano = "soprano"
    contralto = "contralto"
    tenor = "tenor"
    baixo = "baixo"
    na = "na"


class TipoPessoa(str, Enum):
    coralista = "coralista"
    membro = "membro"
    regente = "regente"


class FuncaoTrimestre(str, Enum):
    coralista = "coralista"
    membro = "membro"
    regente = "regente"


class StatusFrequencia(str, Enum):
    presenca = "presenca"
    falta = "falta"
    atraso = "atraso"
    falta_justificada = "falta_justificada"


class Naipe(str, Enum):
    soprano = "soprano"
    contralto = "contralto"
    tenor = "tenor"
    baixo = "baixo"

