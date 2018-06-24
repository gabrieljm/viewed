class Usuario:
    def __init__(self, login, senha, nome, tipo):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.tipo = tipo

class Midia:
    def __init__(self, titulo, genero, ano, sinopse, temporadas, id=None):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.sinopse = sinopse
        self.temporadas = temporadas

class Temporada:
    def __init__(self, id, midiaId):
        self.id = id
        self.midiaId = midiaId

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
    def __init__(self, episodioId, usuarioId):
        self.episodioId = episodioId
        self.usuarioId = usuarioId