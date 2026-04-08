from comunidade import database, login_manager
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from flask_login import UserMixin

#essa é a função que vai carregar o usuario
#precisa do UserMixin que vai deixar o usuario conectado quando sair e voltar
#faz os controles de logoin
#na classe que comanda o usuario tem que colocar o parametro UserMixin
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, unique=True, nullable=False)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='default.jpg')
    posts = relationship("Post", backref="autor", lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    __tablename__ = 'posts'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    #a linha de cima foi substituida pois utcnow foi marcada copmo depreciada a partir do Pytho 3.12
    data_criacao = database.Column(database.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)



