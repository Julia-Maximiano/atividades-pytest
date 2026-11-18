import os 
def test_1_remove_a_variavel(monkeypatch): 
 monkeypatch.delenv("DATABASE_URL") 
assert "DATABASE_URL" not in os.environ 
def test_2_a_variavel_continua_la(): 
 assert "DATABASE_URL" in os.environ 