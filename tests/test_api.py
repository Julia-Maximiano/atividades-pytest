
from fastapi.testclient import TestClient

USUARIO_VALIDO = {
    "nome": "Bruno Lima",
    "email": "bruno@exemplo.com",
    "senha": "senha123"
}


def test_raiz_responde(cliente: TestClient):
    resposta = cliente.get("/")
    assert resposta.status_code == 200


def test_cadastrar_usuario_devolve_201_com_sessao_aberta(cliente: TestClient):
    resposta = cliente.post("/usuarios", json=USUARIO_VALIDO)

    assert resposta.status_code == 201

    corpo = resposta.json()

    assert corpo["accessToken"]
    assert corpo["tokenType"] == "bearer"
    assert corpo["usuario"]["nome"] == "Bruno Lima"
    assert "criadoEm" in corpo["usuario"]


def test_cadastro_nao_expoe_a_senha(cliente: TestClient):
    resposta = cliente.post("/usuarios", json=USUARIO_VALIDO)

    inteiro = resposta.text

    assert "senha123" not in inteiro
    assert "senhaHash" not in inteiro
    assert "senha_hash" not in inteiro

def test_cadastrar_com_email_repetido_devolve_409(cliente: TestClient):
    cliente.post("/usuarios", json=USUARIO_VALIDO)

    resposta = cliente.post("/usuarios", json=USUARIO_VALIDO)

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "E-mail já cadastrado."


def test_email_duplicado_ignora_maiusculas_e_espacos(cliente: TestClient):
    cliente.post("/usuarios", json=USUARIO_VALIDO)

    resposta = cliente.post(
        "/usuarios",
        json={**USUARIO_VALIDO, "email": " BRUNO@Exemplo.com "}
    )

    inteiro = resposta.text

    assert "senha123" not in inteiro
    assert "senhaHash" not in inteiro
    assert "senha_hash" not in i
    assert resposta.status_code == 409


def test_cadastro_nao_expoe_a_senha(cliente: TestClient):
    resposta = cliente.post("/usuarios", json=USUARIO_VALIDO)
nteiro

def test_email_malformado_devolve_422(cliente: TestClient):
    resposta = cliente.post(
        "/usuarios",
        json={**USUARIO_VALIDO, "email": "bruno@"}
    )

    assert resposta.status_code == 422


def test_senha_curta_devolve_422(cliente: TestClient):
    resposta = cliente.post(
        "/usuarios",
        json={**USUARIO_VALIDO, "senha": "123"}
    )

    assert resposta.status_code == 422


