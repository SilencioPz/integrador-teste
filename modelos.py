from shared import db

class Login(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ISBN = db.Column(db.Text, nullable=False) 
    titulo = db.Column(db.Text, nullable=False) 
    autor = db.Column(db.Text, nullable=False)
    editora = db.Column(db.Text, nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.Text, nullable=False) 
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.DECIMAL(10,2), nullable=False) 
    imagem = db.Column(db.Text, nullable=False) 
    palavrinha = db.Column(db.Text, nullable=False)
    
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    opiniao = db.Column(db.Text, nullable=False)
