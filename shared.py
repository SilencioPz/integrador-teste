from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
SECRET_KEY = 'projeto-integrador-2'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bruno:1234@localhost/projeto_web_mer'
app.config['FOTOGRAFIAS_PATH'] = os.path.join(app.root_path, 'static/fotografias')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)