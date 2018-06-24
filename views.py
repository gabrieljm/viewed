from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Midia, Episodio
from dao import MidiaDao, EpisodioDao, UsuarioDao
import time
from helpers import deleta_arquivo, recupera_imagem
from viewed import db, app

midia_dao = MidiaDao(db)
episodio_dao = EpisodioDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = midia_dao.listar()
    nome_imagem = {}
    for item in lista:
        nome_imagem[item.id] = recupera_imagem(item.id)
    return render_template('lista.html', titulo='Mídias', midias=lista, capa_midia=nome_imagem or 'capa_padrao.jpg')


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova Mídia')


@app.route('/criar', methods=['POST',])
def criar():
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

    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Mídia', midia=midia, temporadas=temporadas, capa_midia=nome_imagem or 'capa_padrao.jpg')


@app.route('/atualizar', methods=['POST',])
def atualizar():
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
    midiaId = request.form['midiaId']
    temporadaId = request.form['temporadaId']
    id = request.form['id']
    nome = request.form['nome']
    episodio = Episodio(midiaId, temporadaId, id, nome)
    episodio_dao.criar(episodio)
    return redirect(url_for('editar', id=episodio.midiaId))


@app.route('/atualizarEpisodio', methods=['POST',])
def atualizarEpisodio():
    midiaId = request.form['midiaId']
    temporadaId = request.form['temporadaId']
    id = request.form['id']
    nome = request.form['nome']
    episodio = Episodio(midiaId, temporadaId, id, nome)
    episodio_dao.alterar(episodio)
    return redirect(url_for('editar', id=episodio.midiaId))


@app.route('/deletar/<string:id>')
def deletar(id):
    midia_dao.deletar(id)
    flash('A mídia foi removida com sucesso!')
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
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)