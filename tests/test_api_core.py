from __future__ import annotations

from fastapi.testclient import TestClient


def _nova_pessoa_payload(nome: str, voz: str = "soprano") -> dict:
    return {
        "nome": nome,
        "data_nascimento": "1990-01-01",
        "telefone": "(11) 99999-0000",
        "classificacao_vocal": voz,
        "tipo_padrao": "coralista",
        "foto_url": None,
    }


def _criar_ciclo_trimestre(client: TestClient, ano: int = 2026) -> tuple[str, str]:
    r_ciclo = client.post("/ciclos", json={"ano": ano, "ativo": True, "criar_trimestres": True})
    assert r_ciclo.status_code == 201
    ciclo_id = r_ciclo.json()["id"]

    r_tri = client.get(f"/ciclos/{ciclo_id}/trimestres")
    assert r_tri.status_code == 200
    trimestre_id = r_tri.json()[0]["id"]
    return ciclo_id, trimestre_id


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_pessoas_crud(client: TestClient):
    created = client.post("/pessoas", json=_nova_pessoa_payload("Alice"))
    assert created.status_code == 201
    pessoa_id = created.json()["id"]

    listed = client.get("/pessoas")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["nome"] == "Alice"

    updated = client.put(f"/pessoas/{pessoa_id}", json={"telefone": "(11) 98888-1111"})
    assert updated.status_code == 200
    assert updated.json()["telefone"] == "(11) 98888-1111"

    deleted = client.delete(f"/pessoas/{pessoa_id}")
    assert deleted.status_code == 204

    listed_after = client.get("/pessoas")
    assert listed_after.status_code == 200
    assert listed_after.json() == []


def test_fluxo_ciclo_trimestre_matricula_evento_frequencia(client: TestClient):
    _, trimestre_id = _criar_ciclo_trimestre(client)

    p1 = client.post("/pessoas", json=_nova_pessoa_payload("Maria", "soprano")).json()
    p2 = client.post("/pessoas", json=_nova_pessoa_payload("João", "tenor")).json()

    upsert_matriculas = client.put(
        f"/trimestres/{trimestre_id}/matriculas",
        json={
            "matriculas": [
                {"pessoa_id": p1["id"], "funcao_no_trimestre": "coralista"},
                {"pessoa_id": p2["id"], "funcao_no_trimestre": "coralista"},
            ]
        },
    )
    assert upsert_matriculas.status_code == 200
    assert len(upsert_matriculas.json()) == 2

    r_evento = client.post(
        "/eventos",
        json={
            "trimestre_id": trimestre_id,
            "nome": "Ensaio A",
            "descricao": "Descrição",
            "data_hora": "2026-02-20T19:00:00",
            "tipo": "ensaio_geral",
        },
    )
    assert r_evento.status_code == 201
    evento_id = r_evento.json()["id"]

    r_freq = client.put(
        f"/eventos/{evento_id}/frequencias",
        json={
            "frequencias": [
                {"pessoa_id": p1["id"], "status": "presenca"},
                {"pessoa_id": p2["id"], "status": "falta", "justificativa": "Viagem"},
            ]
        },
    )
    assert r_freq.status_code == 200
    assert len(r_freq.json()) == 2

    listed_freq = client.get(f"/eventos/{evento_id}/frequencias")
    assert listed_freq.status_code == 200
    assert {item["status"] for item in listed_freq.json()} == {"presenca", "falta"}


def test_validacoes_trimestre_invalido_status_invalido_duplicidade(client: TestClient):
    evento_invalid = client.post(
        "/eventos",
        json={
            "trimestre_id": "nao-existe",
            "nome": "Evento inválido",
            "descricao": "",
            "data_hora": "2026-02-20T19:00:00",
        },
    )
    assert evento_invalid.status_code == 404

    r_ciclo = client.post("/ciclos", json={"ano": 2030, "ativo": False, "criar_trimestres": False})
    assert r_ciclo.status_code == 201
    ciclo_id = r_ciclo.json()["id"]

    t1 = client.post("/trimestres", json={"ciclo_id": ciclo_id, "numero": 1})
    assert t1.status_code == 201
    t1_dup = client.post("/trimestres", json={"ciclo_id": ciclo_id, "numero": 1})
    assert t1_dup.status_code == 409

    pessoa = client.post("/pessoas", json=_nova_pessoa_payload("Teste")).json()
    evento = client.post(
        "/eventos",
        json={
            "trimestre_id": t1.json()["id"],
            "nome": "Evento status",
            "descricao": "",
            "data_hora": "2026-03-20T19:00:00",
        },
    ).json()
    status_invalido = client.put(
        f"/eventos/{evento['id']}/frequencias",
        json={"frequencias": [{"pessoa_id": pessoa["id"], "status": "inexistente"}]},
    )
    assert status_invalido.status_code == 422

