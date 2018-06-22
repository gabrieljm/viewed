class Usuario:
    def __init__(self, login, senha, nome, tipo):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.tipo = tipo

class Midia:
    def __init__(self, titulo, genero, ano, sinopse, tipo, id=None):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.sinopse = sinopse
        self.tipo = tipo

class Temporada:
    def __init__(self, id, midiaId):
        self.id = id
        self.midiaId = midiaId

class Episodio:
    def __init__(self, id, temporadaId):
        self.id = id
        self.temporadaId = temporadaId

class Favorito:
    def __init__(self, midiaId, usuarioId):
        self.midiaId = midiaId
        self.usuarioId = usuarioId

class Visto:
    def __init__(self, episodioId, usuarioId):
        self.episodioId = episodioId
        self.usuarioId = usuarioId