import os
from shared import app, db
from wtforms import FileField, SubmitField, HiddenField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, RadioField, validators

class FormularioUsuario(FlaskForm):
    email = StringField('Email:', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha = PasswordField('Senha:', [validators.DataRequired(), validators.Length(min=1, max=60)])
    logar = SubmitField('Logar')

class LivroForm(FlaskForm):
    livro_id = HiddenField('ID do Livro')
    imagem = FileField('Imagem do Livro', validators=[
        FileAllowed(['png'], 'Somente imagens são permitidas!')
    ])
    submit = SubmitField('Enviar')

def recuperaImagem(id):
    for filename in os.listdir(app.config['FOTOGRAFIAS']):
        if f'foto{id}' in filename:
            return filename
    return 'livro.png'

def deletaArquivo(id):
    arquivo = recuperaImagem(id)
    if arquivo != 'livro.png':
        os.remove(os.path.join(app.config['FOTOGRAFIAS'], arquivo))