# Dia 2 — acaba logo senac 
from datetime import date, datetime, timedelta

import pytest

from app.enums import PrioridadeTarefa, StatusTarefa
from app.exceptions import ValorInvalido
from app.models import Tarefa, Usuario


def nova_tarefa(**ajustes):
    dados = {
        "usuario_id": 1,
        "titulo": "Estudar orientação a objetos"
    }

    dados.update(ajustes)

    return Tarefa(**dados)


def test_status_e_somente_leitura():
    tarefa = nova_tarefa()

    with pytest.raises(AttributeError):
        tarefa.status = StatusTarefa.CONCLUIDA

    def test_construtor_nao_aceita_status_como_parametro():
     with pytest.raises(TypeError):
        Tarefa(
            usuario_id=1,
            titulo="X",
            status=StatusTarefa.CONCLUIDA
        )
    def test_construtor_nao_aceita_senha():
     with pytest.raises(TypeError):
        Usuario(
            nome="Ana",
            email="ana@exemplo.com",
            senha="senha123"
        )
    def test_prioridade_invalida_e_recusada():
     with pytest.raises(ValorInvalido):
        nova_tarefa(prioridade="altissima")
    def test_nome_invalido_e_recusado_tambem_depois_da_criacao():
     usuario = novo_usuario()

    with pytest.raises(ValorInvalido):
        usuario.nome = "   "

    def test_concluir_registra_a_data():
     tarefa = nova_tarefa()
    tarefa.concluir()

    assert tarefa.status is StatusTarefa.CONCLUIDA
    assert tarefa.concluido_em is not None

    def test_reabrir_apaga_a_data():
     tarefa = nova_tarefa()
    tarefa.concluir()
    tarefa.reabrir()

    assert tarefa.status is StatusTarefa.PENDENTE
    assert tarefa.concluido_em is None

    def test_editar_outro_campo_nao_mexe_na_data_de_conclusao():
     tarefa = nova_tarefa()
    tarefa.concluir(agora=datetime(2026, 1, 10, 9, 0, 0))

    antes = tarefa.concluido_em
    tarefa.titulo = "Título novo"

    assert tarefa.concluido_em == antes

    def test_definir_status_encaminha_para_a_operacao_correta():
     tarefa = nova_tarefa()

    tarefa.definir_status("concluida")
    assert tarefa.concluido_em is not None

    tarefa.definir_status(StatusTarefa.PENDENTE)
    assert tarefa.concluido_em is None

    def test_tarefa_concluida_nao_esta_atrasada_mesmo_com_prazo_vencido():
     tarefa = nova_tarefa(
        prazo=date.today() - timedelta(days=5)
    )

    tarefa.concluir()

    assert tarefa.esta_atrasada() is False

def test_tarefas_pendentes_filtra_as_concluidas():
    usuario = novo_usuario()

    pendente = nova_tarefa(titulo="Pendente")
    concluida = nova_tarefa(titulo="Concluída")

    concluida.concluir()

    usuario.tarefas = [pendente, concluida]

    assert usuario.tarefas_pendentes() == [pendente]

    def test_concluir_tarefa_ja_concluida_preserva_a_data_original():
     original = datetime(2026, 1, 10, 9, 0, 0)

    tarefa = nova_tarefa()

    tarefa.concluir(agora=original)

    tarefa.concluir(
        agora=datetime(2026, 3, 1, 15, 30, 0)
    )

    assert tarefa.concluido_em == original
