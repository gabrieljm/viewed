class Usuario:
    def __init__(self, nome, login, senha, tipo):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.tipo = tipo

class Midia:
    def __init__(self, titulo, genero, ano, sinopse, temporadas, id=None):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.sinopse = sinopse
        self.temporadas = temporadas

class Episodio:
    def __init__(self, midiaId, temporadaId, id, nome):
        self.midiaId = midiaId
        self.temporadaId = temporadaId
        self.id = id
        self.nome = nome

class Favorito:
    def __init__(self, midiaId, usuarioId):
        self.midiaId = midiaId
        self.usuarioId = usuarioId

class Visto:
    def __init__(self, usuarioId, midiaId, temporadaId, episodioId):
        self.usuarioId = usuarioId
        self.midiaId = midiaId
        self.temporadaId = temporadaId
        self.episodioId = episodioId
