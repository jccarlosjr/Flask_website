from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))



#Criando uma classe herdando da classe 'Model' do SQLAlchemy
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=False)
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
        return len(self.posts)

#primary_key=True define como a chave primária no banco de dados
#nullable=False impede que o campo esteja vazio
#unique=True define que não podem ter 2 indices no banco de dados com esse o mesmo valor


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


#datetime.utcnow sem os parenteses, vai passar a função em si ao invés de passar a data da criação do código

