from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Midia, Episodio, Visto, Favorito, Usuario
from dao import MidiaDao, EpisodioDao, VistoDao, FavoritoDao, UsuarioDao
import time
from helpers import deleta_arquivo, recupera_imagem
from viewed import db, app

midia_dao = MidiaDao(db)
episodio_dao = EpisodioDao(db)
visto_dao = VistoDao(db)
favorito_dao = FavoritoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    lista = midia_dao.listar()
    nome_imagem = {}
    for item in lista:
        nome_imagem[item.id] = recupera_imagem(item.id)

    favoritos = favorito_dao.buscar(session['usuario_logado'])

    listaFavoritos = []

    for midia in lista:
        if midia.id in favoritos:
            listaFavoritos.append(midia)

    if session['tipo_usuario'] == 'A':
        return render_template('lista.html', titulo='Seriados', midias=lista, capa_midia=nome_imagem or 'capa_padrao.jpg')
    return render_template('listaUser.html', titulo='Seriados', midias=lista, midiasFavoritas=listaFavoritos, favoritos=favoritos, capa_midia=nome_imagem or 'capa_padrao.jpg')


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    return render_template('novo.html', titulo='Nova Mídia')


@app.route('/criar', methods=['POST',])
def criar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    titulo = request.form['titulo']
    genero = request.form['genero']
    ano = request.form['ano']
    sinopse = request.form['sinopse']
    temporadas = request.form['temporadas']
    midia = Midia(titulo, genero, ano, sinopse, temporadas)
    midia = midia_dao.salvar(midia)

    if request.files['arquivo']:
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{upload_path}/capa{midia.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))

    midia = midia_dao.busca_por_id(id)
    temporadas = []

    for temporadaId in range(1, midia.temporadas):
        episodios = episodio_dao.listar(id, temporadaId)
        temporadas.append(episodios)

    vistos = visto_dao.buscarPorMidia(session['usuario_logado'], midia.id)

    nome_imagem = recupera_imagem(id)

    if session['tipo_usuario'] == 'A':
        return render_template('editar.html', titulo='Editando Mídia', midia=midia, temporadas=temporadas, capa_midia=nome_imagem or 'capa_padrao.jpg')
    return render_template('editarUser.html', titulo=midia.titulo, midia=midia, temporadas=temporadas, vistos=vistos, capa_midia=nome_imagem or 'capa_padrao.jpg')


@app.route('/visto/<string:usuarioId>/<string:midiaId>/<string:temporadaId>/<string:id>')
def visto(usuarioId, midiaId, temporadaId, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    visto = Visto(usuarioId, midiaId, temporadaId, id)
    visto_dao.marcar_visto(visto)
    return redirect(url_for('editar', id=midiaId))


@app.route('/favoritar/<string:midiaId>/<string:usuarioId>')
def favoritar(midiaId, usuarioId):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    favorito = Favorito(midiaId, usuarioId)
    favorito_dao.favoritar(favorito)
    return redirect(url_for('index'))


@app.route('/atualizar', methods=['POST',])
def atualizar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    titulo = request.form['titulo']
    genero = request.form['genero']
    ano = request.form['ano']
    sinopse = request.form['sinopse']
    temporadas = request.form['temporadas']
    midia = Midia(titulo, genero, ano, sinopse, temporadas, id=request.form['id'])
    arquivo = request.files.get('arquivo')

    if arquivo:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(midia.id)
        arquivo.save(f'{upload_path}/capa{midia.id}-{timestamp}.jpg')

    midia_dao.salvar(midia)
    return redirect(url_for('index'))


@app.route('/criarEpisodio', methods=['POST',])
def criarEpisodio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    midiaId = request.form['midiaId']
    temporadaId = request.form['temporadaId']
    id = request.form['id']
    nome = request.form['nome']
    episodio = Episodio(midiaId, temporadaId, id, nome)
    episodio_dao.criar(episodio)
    return redirect(url_for('editar', id=episodio.midiaId))


@app.route('/atualizarEpisodio', methods=['POST',])
def atualizarEpisodio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    midiaId = request.form['midiaId']
    temporadaId = request.form['temporadaId']
    id = request.form['id']
    nome = request.form['nome']
    episodio = Episodio(midiaId, temporadaId, id, nome)
    episodio_dao.alterar(episodio)
    return redirect(url_for('editar', id=episodio.midiaId))


@app.route('/deletarEpisodio/<string:midiaId>/<string:temporadaId>/<string:id>')
def deletarEpisodio(midiaId, temporadaId, id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    episodio_dao.deletar(midiaId, temporadaId, id)
    return redirect(url_for('editar', id=midiaId))


@app.route('/deletar/<string:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    midia_dao.deletar(id)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_login(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.login
            session['nome_usuario'] = usuario.nome
            session['tipo_usuario'] = usuario.tipo
            return redirect(url_for('index'))
        else:
            flash('Senha incorreta!')
            return redirect(url_for('login'))
    else:
        flash('Usuário inexistente!')
        return redirect(url_for('login'))


@app.route('/registrar', methods=['POST',])
def registrar():
    nome = request.form['nome']
    login = request.form['login']
    senha = request.form['senha']
    tipo = request.form['tipo']
    usuario = Usuario(nome, login, senha, tipo)
    usuario_dao.registrar(usuario)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session['nome_usuario'] = None
    session['tipo_usuario'] = None
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)