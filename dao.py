from models import Usuario, Midia, Temporada, Episodio, Favorito, Visto

SQL_DELETA_MIDIA = 'DELETE from midia where id = %s'
SQL_MIDIA_POR_ID = 'SELECT * from midia where id = %s'
SQL_USUARIO_POR_LOGIN = 'SELECT * from usuario where login = %s'
SQL_ATUALIZA_MIDIA = 'UPDATE midia SET titulo=%s, genero=%s, ano=%s, sinopse=%s, tipo=%s where id = %s'
SQL_BUSCA_MIDIAS = 'SELECT * from midia'
SQL_CRIA_MIDIA = 'INSERT into midia (titulo, genero, ano, sinopse, tipo) values (%s, %s, %s, %s, %s)'


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
                midia.tipo,
                midia.id
            ))
        else:
            cursor.execute(SQL_CRIA_MIDIA, (
                midia.titulo,
                midia.genero,
                midia.ano,
                midia.sinopse,
                midia.tipo
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


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
