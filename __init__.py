from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)


app.config['SECRET_KEY'] = '97567c167a9cc2002d29d420bd91834e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #Define q as páginas com decorator @login_required sejam direcionadas p/ a função login
login_manager.login_message = 'Faça login para ver essa página' #Altera a mensagem de erro ao tentar acessar uma página restrita pelo @login_required
login_manager.login_message_category = 'alert-info' #Aplica a classe alert-info do bootstrap na mensagem de erro

from comunidadeimpressionadora import routes


