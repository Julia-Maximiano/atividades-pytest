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