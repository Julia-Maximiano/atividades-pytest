
from fastapi.testclient import TestClient
from datetime import date, timedelta

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



def test_consultar_a_propria_conta_devolve_o_usuario_do_token(
    cliente_logado: TestClient, usuario: dict
):
    resposta = cliente_logado.get("/usuarios/eu")

    assert resposta.status_code == 200
    assert resposta.json() == usuario


def test_criar_tarefa_nasce_pendente(
    cliente_logado: TestClient, usuario: dict
):
    resposta = cliente_logado.post(
        "/tasks",
        json={
            "titulo": "Entregar o relatório",
            "prioridade": "alta",
            "prazo": str(date.today() + timedelta(days=30))
        }
    )

    assert resposta.status_code == 201

    corpo = resposta.json()

    assert corpo["status"] == "pendente"
    assert corpo["concluidoEm"] is None
    assert corpo["usuarioId"] == usuario["id"]


def test_criar_tarefa_sem_token_devolve_401(cliente: TestClient):
    resposta = cliente.post("/tasks", json={"titulo": "X"})

    assert resposta.status_code == 401


def test_criar_tarefa_com_prioridade_invalida_devolve_422(
    cliente_logado: TestClient
):
    resposta = cliente_logado.post(
        "/tasks",
        json={"titulo": "X", "prioridade": "altissima"}
    )

    assert resposta.status_code == 422


def test_listar_tarefas_de_usuario_sem_tarefas_devolve_lista_vazia(
    cliente_logado: TestClient
):
    resposta = cliente_logado.get("/tasks")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_filtra_por_status(cliente_logado: TestClient):
    for titulo in ("A", "B"):
        cliente_logado.post("/tasks", json={"titulo": titulo})

    primeira = cliente_logado.get("/tasks").json()[0]

    cliente_logado.patch(
        f"/tasks/{primeira['id']}",
        json={"status": "concluida"}
    )

    pendentes = cliente_logado.get(
        "/tasks?status=pendente"
    ).json()

    assert len(pendentes) == 1
    assert pendentes[0]["status"] == "pendente"


def test_listar_ordena_por_prioridade_da_mais_urgente_para_a_menos(
    cliente_logado: TestClient
):
    for prioridade in ("baixa", "urgente", "media"):
        cliente_logado.post(
            "/tasks",
            json={"titulo": prioridade, "prioridade": prioridade}
        )

    resposta = cliente_logado.get(
        "/tasks?ordenarPor=prioridade&ordem=asc"
    )

    assert [t["prioridade"] for t in resposta.json()] == [
        "urgente", "media", "baixa"
    ]


def test_campo_de_ordenacao_invalido_devolve_422(
    cliente_logado: TestClient
):
    resposta = cliente_logado.get(
        "/tasks?ordenarPor=inventado"
    )

    assert resposta.status_code == 422


def test_filtrar_por_prazo_ate(cliente_logado: TestClient):
    hoje = date.today()

    cliente_logado.post(
        "/tasks",
        json={
            "titulo": "Vence logo",
            "prazo": str(hoje + timedelta(days=1))
        }
    )

    cliente_logado.post(
        "/tasks",
        json={
            "titulo": "Vence tarde",
            "prazo": str(hoje + timedelta(days=30))
        }
    )

    resposta = cliente_logado.get(
        f"/tasks?prazoAte={hoje + timedelta(days=7)}"
    )

    assert [t["titulo"] for t in resposta.json()] == ["Vence logo"]


def test_concluir_tarefa_preenche_a_data(cliente_logado: TestClient):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Concluir"}
    ).json()

    resposta = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"status": "concluida"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["concluidoEm"] is not None


def test_reabrir_tarefa_limpa_a_data(cliente_logado: TestClient):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Reabrir"}
    ).json()

    cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"status": "concluida"}
    )

    resposta = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"status": "pendente"}
    )

    assert resposta.json()["concluidoEm"] is None


def test_editar_titulo_de_tarefa_concluida_preserva_a_data(
    cliente_logado: TestClient
):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Original"}
    ).json()

    concluida = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"status": "concluida"}
    ).json()

    editada = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"titulo": "Título novo"}
    ).json()

    assert editada["titulo"] == "Título novo"
    assert editada["concluidoEm"] == concluida["concluidoEm"]


def test_apagar_o_prazo_e_diferente_de_nao_informar(
    cliente_logado: TestClient
):
    prazo = str(date.today() + timedelta(days=10))

    criada = cliente_logado.post(
        "/tasks",
        json={"titulo": "Com prazo", "prazo": prazo}
    ).json()

    sem_mencionar = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"titulo": "Outro título"}
    ).json()

    assert sem_mencionar["prazo"] == prazo

    apagando = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"prazo": None}
    ).json()

    assert apagando["prazo"] is None


def test_atualizar_tarefa_inexistente_devolve_404(
    cliente_logado: TestClient
):
    resposta = cliente_logado.patch(
        "/tasks/9999",
        json={"status": "concluida"}
    )

    assert resposta.status_code == 404


def test_titulo_vazio_no_patch_devolve_422(cliente_logado: TestClient):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Original"}
    ).json()

    resposta = cliente_logado.patch(
        f"/tasks/{criada['id']}",
        json={"titulo": "                       "}
    )

    assert resposta.status_code == 422


def test_remover_tarefa_devolve_204_sem_corpo(
    cliente_logado: TestClient
):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Remover"}
    ).json()

    resposta = cliente_logado.delete(
        f"/tasks/{criada['id']}"
    )

    assert resposta.status_code == 204
    assert resposta.content == b""


def test_remover_a_mesma_tarefa_duas_vezes_devolve_404(
    cliente_logado: TestClient
):
    criada = cliente_logado.post(
        "/tasks", json={"titulo": "Remover"}
    ).json()

    cliente_logado.delete(f"/tasks/{criada['id']}")

    assert cliente_logado.delete(
        f"/tasks/{criada['id']}"
    ).status_code == 404
