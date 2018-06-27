from models import Usuario, Midia, Episodio, Favorito, Visto

SQL_DELETA_MIDIA = 'DELETE from midia where id = %s'
SQL_MIDIA_POR_ID = 'SELECT * from midia where id = %s'
SQL_USUARIO_POR_LOGIN = 'SELECT nome, login, senha, tipo from usuario where login = %s'
SQL_ATUALIZA_MIDIA = 'UPDATE midia SET titulo=%s, genero=%s, ano=%s, sinopse=%s, temporadas=%s where id = %s'
SQL_BUSCA_MIDIAS = 'SELECT * from midia'
SQL_CRIA_MIDIA = 'INSERT into midia (titulo, genero, ano, sinopse, temporadas) values (%s, %s, %s, %s, %s)'
SQL_BUSCA_EPISODIOS = 'SELECT midiaId, temporadaId, id, nome FROM episodio WHERE midiaId = %s AND temporadaId = %s'
SQL_CRIA_EPISODIO = 'INSERT into episodio (midiaId, temporadaId, id, nome) values (%s, %s, %s, %s)'
SQL_ATUALIZA_EPISODIO = 'UPDATE episodio SET nome=%s WHERE midiaId=%s AND temporadaId=%s and id=%s'
SQL_DELETA_EPISODIO = 'DELETE FROM episodio where midiaId = %s AND temporadaId = %s AND id = %s'
SQL_EPISODIO_POR_ID = 'SELECT nome FROM episodio WHERE midiaId=%s AND temporadaId=%s AND id=%s'
SQL_CRIA_VISTO = 'INSERT INTO visto (usuarioId, midiaId, temporadaId, episodioId) values (%s, %s, %s, %s)'
SQL_BUSCA_VISTO = 'SELECT * FROM visto WHERE usuarioId=%s AND midiaId=%s AND temporadaId=%s AND episodioId=%s'
SQL_BUSCA_VISTO_POR_TEMPORADA = 'SELECT * FROM visto WHERE usuarioId=%s AND midiaId=%s AND temporadaId=%s'
SQL_BUSCA_VISTO_POR_MIDIA = 'SELECT usuarioId, midiaId, temporadaId, episodioId FROM visto WHERE usuarioId=%s AND midiaId=%s'
SQL_DELETA_VISTO = 'DELETE FROM visto WHERE usuarioId=%s AND midiaId=%s AND temporadaId=%s AND episodioId=%s'
SQL_REGISTRA_USUARIO = 'INSERT INTO usuario (nome, login, senha, tipo) values (%s, %s, %s, %s)'
SQL_ADICIONA_FAVORITO = 'INSERT INTO favorito (midiaId, usuarioId) values (%s, %s)'
SQL_REMOVE_FAVORITO = 'DELETE FROM favorito WHERE midiaId = %s AND usuarioId = %s'
SQL_BUSCA_FAVORITOS_POR_MIDIA = 'SELECT midiaId FROM favorito WHERE usuarioId = %s'
SQL_BUSCA_FAVORITO = 'SELECT * FROM favorito WHERE midiaId = %s and usuarioId = %s'


class MidiaDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, midia):
        cursor = self.__db.connection.cursor()

        if (midia.id):
            cursor.execute(SQL_ATUALIZA_MIDIA, (
                midia.titulo,
                midia.genero,
                midia.ano,
                midia.sinopse,
                midia.temporadas,
                midia.id
            ))
        else:
            cursor.execute(SQL_CRIA_MIDIA, (
                midia.titulo,
                midia.genero,
                midia.ano,
                midia.sinopse,
                midia.temporadas
            ))
            midia.id = cursor.lastrowid
        self.__db.connection.commit()
        return midia

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_MIDIAS)
        midias = traduz_midias(cursor.fetchall())
        return midias

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_MIDIA_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Midia(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_MIDIA, (id, ))
        self.__db.connection.commit()


class EpisodioDao:
    def __init__(self, db):
        self.__db = db

    def criar(self, episodio):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_CRIA_EPISODIO, (
            episodio.midiaId,
            episodio.temporadaId,
            episodio.id,
            episodio.nome
        ))
        self.__db.connection.commit()
        return episodio

    def alterar(self, episodio):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_ATUALIZA_EPISODIO, (
            episodio.nome,
            episodio.midiaId,
            episodio.temporadaId,
            episodio.id
        ))
        self.__db.connection.commit()
        return episodio

    def listar(self, midiaId, temporadaId):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_EPISODIOS, (midiaId, temporadaId,))
        episodios = traduz_episodios(cursor.fetchall())
        return episodios

    def busca_por_id(self, midiaId, temporadaId, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_EPISODIO_POR_ID, (midiaId, temporadaId, id,))
        tupla = cursor.fetchone()
        return Episodio(midiaId, temporadaId, id, tupla[0])

    def deletar(self, midiaId, temporadaId, id):
        self.__db.connection.cursor().execute(SQL_DELETA_EPISODIO, (midiaId, temporadaId, id,))
        self.__db.connection.commit()


class VistoDao:
    def __init__(self, db):
        self.__db = db

    def marcar_visto(self, visto):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_BUSCA_VISTO, (
            visto.usuarioId,
            visto.midiaId,
            visto.temporadaId,
            visto.episodioId
        ))
        vistoExiste = cursor.fetchone()
        if vistoExiste:
            cursor.execute(SQL_DELETA_VISTO, (
                visto.usuarioId,
                visto.midiaId,
                visto.temporadaId,
                visto.episodioId
            ))
        else:
            cursor.execute(SQL_CRIA_VISTO, (
                visto.usuarioId,
                visto.midiaId,
                visto.temporadaId,
                visto.episodioId
            ))
        self.__db.connection.commit()

    def buscarPorMidia(self, usuarioId, midiaId):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_VISTO_POR_MIDIA, (
            usuarioId,
            midiaId
        ))
        vistos = traduz_vistos(cursor.fetchall())
        return vistos


class FavoritoDao:
    def __init__(self, db):
        self.__db = db

    def favoritar(self, favorito):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_BUSCA_FAVORITO, (
            favorito.midiaId,
            favorito.usuarioId
        ))
        favoritoExiste = cursor.fetchone()
        if favoritoExiste:
            cursor.execute(SQL_REMOVE_FAVORITO, (
                favorito.midiaId,
                favorito.usuarioId
            ))
        else:
            cursor.execute(SQL_ADICIONA_FAVORITO, (
                favorito.midiaId,
                favorito.usuarioId
            ))
        self.__db.connection.commit()

    def buscar(self, usuarioId):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_FAVORITOS_POR_MIDIA, (usuarioId,))
        favoritos = traduz_favoritos(cursor.fetchall())

        return favoritos


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def registrar(self, usuario):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_REGISTRA_USUARIO, (
            usuario.nome,
            usuario.login,
            usuario.senha,
            usuario.tipo
        ))
        self.__db.connection.commit()
        return usuario

    def buscar_por_login(self, login):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_LOGIN, (login,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_midias(midias):
    def cria_midia_com_tupla(tupla):
        return Midia(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    return list(map(cria_midia_com_tupla, midias))


def traduz_episodios(episodios):
    def cria_episodio_com_tupla(tupla):
        return Episodio(tupla[0], tupla[1], tupla[2], tupla[3])
    return list(map(cria_episodio_com_tupla, episodios))


def traduz_vistos(vistos):
    def cria_visto_com_tupla(tupla):
        return Visto(tupla[0], tupla[1], tupla[2], tupla[3])
    return list(map(cria_visto_com_tupla, vistos))


def traduz_favoritos(favoritos):
    def cria_midiaId_com_tupla(tupla):
        return tupla[0]
    return list(map(cria_midiaId_com_tupla, favoritos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
