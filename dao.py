from models import Usuario, Midia, Temporada, Episodio, Favorito, Visto

SQL_DELETA_MIDIA = 'DELETE from midia where id = %s'
SQL_MIDIA_POR_ID = 'SELECT * from midia where id = %s'
SQL_USUARIO_POR_LOGIN = 'SELECT * from usuario where login = %s'
SQL_ATUALIZA_MIDIA = 'UPDATE midia SET titulo=%s, genero=%s, ano=%s, sinopse=%s, temporadas=%s where id = %s'
SQL_BUSCA_MIDIAS = 'SELECT * from midia'
SQL_CRIA_MIDIA = 'INSERT into midia (titulo, genero, ano, sinopse, temporadas) values (%s, %s, %s, %s, %s)'
SQL_BUSCA_EPISODIOS = 'SELECT midiaId, temporadaId, id, nome FROM episodio WHERE midiaId = %s AND temporadaId = %s'
SQL_CRIA_EPISODIO = 'INSERT into episodio (midiaId, temporadaId, id, nome) values (%s, %s, %s, %s)'
SQL_ATUALIZA_EPISODIO = 'UPDATE episodio SET nome=%s WHERE midiaId=%s AND temporadaId=%s and id=%s'
SQL_DELETA_EPISODIO = 'DELETE FROM episodio where midiaId = %s AND temporadaId = %s AND id = %s'
SQL_EPISODIO_POR_ID = 'SELECT nome FROM episodio WHERE midiaId=%s AND temporadaId=%s AND id=%s'


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


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

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


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
