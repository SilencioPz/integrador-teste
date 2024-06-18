from flask import request, flash, redirect, url_for, render_template, session
from shared import app, db
from modelos import Login, Livro, Feedback
from funcoes import *
from werkzeug.utils import secure_filename

@app.route('/crud_login', methods=['GET', 'POST'])
def crud_login():
    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'create':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            novo_usuario = Login(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário criado com sucesso!')

        elif operation == 'read':
            usuarios = Login.query.all()
            flash('Usuário lido com sucesso!')
            return render_template('lista_usuarios.html', usuarios=usuarios)

        elif operation == 'update':
            id = request.form.get('id')
            novo_nome = request.form.get('nome')
            novo_email = request.form.get('email')
            nova_senha = request.form.get('senha')
            usuario = Login.query.get(id)
            usuario.nome = novo_nome
            usuario.email = novo_email
            usuario.senha = nova_senha
            db.session.commit()
            flash('Usuário atualizado com sucesso!')

        elif operation == 'delete':
            id = request.form.get('id')
            usuario = Login.query.get(id)
            db.session.delete(usuario)
            db.session.commit()
            flash('Usuário deletado com sucesso!')

    return render_template('crud_login.html')

@app.route('/delete_usuario/<int:id>', methods=['POST'])
def delete_usuario(id):
    # Deleta entradas em Feedback
    Feedback.query.filter_by(usuario_id=id).delete()

    # Deleta entradas em Livros
    Livro.query.filter_by(usuario_id=id).delete()

    # Depois, delete o usuário
    Login.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('crud_login'))

@app.route('/crud_livros', methods=['GET', 'POST'])
def crud_livros():
    form = LivroForm()
    if form.validate_on_submit(): 
        operation = request.form.get('operation')
    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'create':
            usuario_id = session.get('usuario_id')
            ISBN = request.form.get('ISBN')
            titulo = request.form.get('titulo')
            autor = request.form.get('autor')
            editora = request.form.get('editora')
            ano_publicacao = request.form.get('ano_publicacao')
            categoria = request.form.get('categoria')
            quantidade = request.form.get('quantidade')
            preco = request.form.get('preco')
            imagem = request.form.get('imagem')
            palavrinha = request.form.get('palavrinha')

            livro = Livro.query.filter_by(titulo=titulo).first()
            if livro:
                flash('Livro já cadastrado!')
                return redirect(url_for('crud_livros'))

            novoLivro = Livro(usuario_id=usuario_id, ISBN=ISBN, titulo=titulo, autor=autor, editora=editora,
                            ano_publicacao=ano_publicacao, categoria=categoria, quantidade=quantidade,
                            preco=preco, imagem=imagem, palavrinha=palavrinha)
            db.session.add(novoLivro)
            db.session.commit()
            flash('Livro adicionado com sucesso!')

        elif operation == 'read':
            livros = Livro.query.all()
            return render_template('lista_livros.html', livros=livros, form=form)

        elif operation == 'update':
            if form.validate_on_submit():  
                livro_id = form.livro_id.data  
                livro = Livro.query.get(livro_id)
        if livro:
            livro.ISBN = form.ISBN.data 
            livro.titulo = form.titulo.data
            livro.autor = form.autor.data
            livro.editora = form.editora.data
            livro.ano_publicacao = form.ano_publicacao.data
            livro.categoria = form.categoria.data
            livro.quantidade = form.quantidade.data
            livro.preco = form.preco.data
            if form.imagem.data:
                nome_imagem = secure_filename(form.imagem.data.filename)
                form.imagem.data.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem))
                livro.imagem = nome_imagem  # Salva o nome da nova imagem
            db.session.commit()
            flash('Livro atualizado com sucesso!')

        elif operation == 'delete':
            livro_id = LivroForm.livro_id.data
            livro = Livro.query.get(livro_id)
            if livro:
                db.session.delete(livro)
                db.session.commit()
                flash('Livro deletado com sucesso!')

    return render_template('crud_livros.html', form=form)