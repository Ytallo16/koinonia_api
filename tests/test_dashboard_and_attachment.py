from __future__ import annotations

from fastapi.testclient import TestClient


def _pessoa(nome: str, voz: str) -> dict:
    return {
        "nome": nome,
        "data_nascimento": "1992-05-05",
        "telefone": "(11) 97777-0000",
        "classificacao_vocal": voz,
        "tipo_padrao": "coralista",
    }


def _setup_evento(client: TestClient) -> tuple[str, str, str]:
    ciclo = client.post("/ciclos", json={"ano": 2026, "ativo": True, "criar_trimestres": True}).json()
    trimestres = client.get(f"/ciclos/{ciclo['id']}/trimestres").json()
    trimestre_id = trimestres[0]["id"]
    evento = client.post(
        "/eventos",
        json={
            "trimestre_id": trimestre_id,
            "nome": "Ensaio principal",
            "descricao": "teste",
            "data_hora": "2026-04-02T19:30:00",
        },
    ).json()
    return ciclo["id"], trimestre_id, evento["id"]


def test_dashboard_agregacoes(client: TestClient):
    _, _, evento_id = _setup_evento(client)

    soprano = client.post("/pessoas", json=_pessoa("Soprano 1", "soprano")).json()
    tenor = client.post("/pessoas", json=_pessoa("Tenor 1", "tenor")).json()

    r_freq = client.put(
        f"/eventos/{evento_id}/frequencias",
        json={
            "frequencias": [
                {"pessoa_id": soprano["id"], "status": "presenca"},
                {"pessoa_id": tenor["id"], "status": "atraso"},
            ]
        },
    )
    assert r_freq.status_code == 200

    resumo = client.get("/dashboard/resumo?ano=2026&trimestre=1")
    assert resumo.status_code == 200
    data = resumo.json()
    assert data["eventos"] == 1
    assert data["presencas"] == 2
    assert data["faltas"] == 0

    coralistas = client.get("/dashboard/coralistas?ano=2026&trimestre=1")
    assert coralistas.status_code == 200
    assert len(coralistas.json()) == 2
    assert all(item["percentual_presenca"] == 100 for item in coralistas.json())

    naipes = client.get("/dashboard/naipes?ano=2026&trimestre=1")
    assert naipes.status_code == 200
    as_dict = {item["naipe"]: item for item in naipes.json()}
    assert as_dict["soprano"]["membros"] == 1
    assert as_dict["tenor"]["membros"] == 1


def test_upload_download_delete_anexo(client: TestClient):
    _, _, evento_id = _setup_evento(client)

    upload = client.post(
        f"/eventos/{evento_id}/anexo",
        files={"file": ("teste.txt", b"conteudo do anexo", "text/plain")},
    )
    assert upload.status_code == 200
    assert upload.json()["anexo_nome"] == "teste.txt"

    download = client.get(f"/eventos/{evento_id}/anexo")
    assert download.status_code == 200
    assert download.content == b"conteudo do anexo"

    removed = client.delete(f"/eventos/{evento_id}/anexo")
    assert removed.status_code == 200
    assert removed.json()["anexo_storage_path"] is None

