import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "segredo-de-teste-nao-usar-em-producao"

import pytest
from sqlalchemy.orm import Session
from app.database import Base, SessionLocal, criar_tabelas, engine
from app.security import HashBcrypt

@pytest.fixture
def hasher():
    return HashBcrypt(custo=4)

@pytest.fixture(autouse=True)
def banco_limpo():
    Base.metadata.drop_all(bind=engine)
    criar_tabelas()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sessao() -> Session:
    sessao = SessionLocal()

    try:
        yield sessao
    finally:
        sessao.rollback()
        sessao.close()
