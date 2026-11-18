
from app.models import Usuario


def test_a_cria_um_usuario(sessao):
    usuario = Usuario(nome="Ana", email="ana@exemplo.com")
    usuario._senha_hash = "hash-qualquer"

    sessao.add(usuario)
    sessao.commit()


def test_b_o_banco_comeca_vazio(sessao):
    assert sessao.query(Usuario).count() == 0

