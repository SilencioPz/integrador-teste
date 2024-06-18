import mysql.connector, time, os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from shared import app, db, SECRET_KEY
from modelos import *
from funcoes import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from admin_credentials import ADMIN_USERNAME, ADMIN_PASSWORD
import crud
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def test_connection():
    connection = None
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
    except Exception as e:
        print("Erro ao conectar com o banco de dados: ", e)
        return False
    else:
        print("Conectado com sucesso!")
        return True
    finally:
        if connection:  # Verifique se connection não é None antes de fechar
            connection.close()

@app.route('/')
def novouser():
    if test_connection():
        flash('Conexão com o banco de dados estabelecida com sucesso!')
    else:
        flash('Falha ao conectar com o banco de dados.')
        
    return render_template('novouser.html', titulo='Novo Usuário Quié Isso Livros:')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormularioUsuario()
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        # Busca o usuário pelo e-mail fornecido
        usuario = Login.query.filter_by(email=email).first()
        
        # Verifica usuário e senha
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            # Armazena o ID do usuário na sessão
            session['usuario_id'] = usuario.id
            # Se ok, à página principal
            return redirect(url_for('principal'))
        else:
            flash('E-mail ou senha inválidos.')
            
    proxima = request.args.get('proxima')
    return render_template('login.html', form=form, proxima=proxima)

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Cria o hash da senha
    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
    
    carinha = Login(nome=nome, email=email, senha=hashed_senha)
    db.session.add(carinha)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/principal')
def principal():
    if 'usuario_id' not in session:
        return redirect(url_for('login', proxima=url_for('principal')))
    else:
        form = LivroForm() 
        return render_template('principal.html', titulo='Quié Isso Livros', form=form) 

@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Login.query.filter_by(email=form.email.data).first()
    if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
        # Armazena o ID do usuário na sessão
        session['usuario_id'] = usuario.id
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('principal'))
    elif usuario:
        flash('Senha incorreta.')
    else:
        flash('Usuário não encontrado.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # ID do usuário atual é removido
    session.pop('usuario_id', None)
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))

@app.route('/fotografias/<filename>')
def imagem(filename):
    try:
        image_path = os.path.join(app.config['FOTOGRAFIAS_PATH'], filename)
        return send_file(image_path, mimetype='image/png')
    except FileNotFoundError:
        flash('Imagem não encontrada.')
        return redirect(url_for('lista_livros'))
    
@app.route('/confirmar', methods=['POST'])
def confirmar():
    form = LivroForm()
    if form.validate_on_submit():
        livro_id = form.livro_id.data
        livro = Livro.query.get(livro_id)
        if livro:
            livro.imagemCaminho = url_for('fotografias', filename=livro.imagem) if livro.imagem else url_for('static', filename='livro.png')
            session['livro_id'] = livro_id
            return render_template('confirmar.html', livro=livro, form=form)
        else:
            flash('Livro não encontrado!', 'danger')
            return redirect(url_for('lista_livros'))
    return redirect(url_for('login')) 

@app.route('/carrossel')
def carrossel():
    imagens = Livro.query.all()
    return render_template('carrossel.html', imagens=imagens)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se é ou não um ADM
        usuario_obj = Login.query.filter_by(email=username).first()
        if usuario_obj and password == usuario_obj.senha:
            session['admin_logged_in'] = True
            flash('Login de administrador bem-sucedido!')
            return redirect(url_for('crudlogin'))
        else:
            flash('Credenciais de administrador incorretas.')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logout de administrador realizado com sucesso!')
    return redirect(url_for('login'))

#Rota da barra de pesquisa, para facilidades
@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    if request.method == 'POST':
        termo_pesquisa = request.form.get('termo_pesquisa')
    else:
        termo_pesquisa = request.args.get('pesquisa')
    resultados = Livro.query.filter(Livro.nome.contains(termo_pesquisa)).all()
    if not resultados:
        return render_template('resultados.html', resultados="pesquisa não encontrada")
    else:
        return render_template('resultados.html', resultados=resultados)

#Rota dos comentários dos usuários
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        usuario_id = session.get('usuario_id')  

        novo_feedback = Feedback(usuario_id=usuario_id, opiniao=feedback)
        db.session.add(novo_feedback)
        db.session.commit()
        return 'Obrigado pelo seu feedback!'
    return render_template('feedback.html')

#Rota para as categorias de livros do site
@app.route('/livros/<categoria>')
def livros_categoria(categoria):
    # Limite de 7 livros por categoria 
    livros = Livro.query.filter_by(categoria=categoria).limit(7).all()
    return render_template('seu_template.html', livros=livros, categoria=categoria)

@app.route('/formulario')
def escolhe_livros():
    form = LivroForm()
    listaLivros = Livro.query.all()
    livros = []
    for livro in listaLivros:
        livro.imagemCaminho = url_for('imagem', filename=livro.imagem) if livro.imagem else url_for('static', filename='default.png')
        livros.append((str(livro.id), livro.titulo))
    form.candidato_id.choices = livros
    return render_template('escolhe_livros.html', titulo='Lista de Livros', livros=listaLivros, form=form)

@app.route('/lista_livros')
def lista_livros():
    form = LivroForm()
    livros = Livro.query.all()
    return render_template('lista_livros.html', form=form, livros=livros)

if __name__ == '__main__':
    app.run(debug=True)