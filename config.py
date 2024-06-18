import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from shared import app, db

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        usuario = 'bruno',
        senha = '1234',
        servidor = 'localhost',
        database = 'projeto_web_mer'
    )
    
app.config['FOTOGRAFIAS_PATH'] = os.path.join(app.root_path, 'static/fotografias')