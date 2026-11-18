import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "segredo-de-teste-nao-usar-em-producao"

import pytest

from app.security import HashBcrypt

@pytest.fixture
def hasher():
    return HashBcrypt(custo=4)

