#para criar o banco de dados no flask pelo arquivo .py
#e fazer teste de gravação e buscas

from comunidade import app, database
from comunidade.models import Usuario, Post

#para criar o banco de dados no flask executar o .py
with app.app_context():
    database.create_all()


#para cadastrar algo no banco de dados
# with app.app_context():
#     usuario = Usuario(username = 'Marcelo',email = '1@m.com.br', senha = '123456')
#     usuario2 = Usuario(username = 'João',email = '2@m.com.br', senha = '123456')
#     usuario3 = Usuario(username = 'Ana',email = '3@m.com.br', senha = '123456')
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.add(usuario3)
#     database.session.commit()

# with app.app_context():
#     meus_usuario = Usuario.query.all()
#     lista_usuario = []
#     for usuario in meus_usuario:
#         lista_usuario.append(usuario.id)
#         lista_usuario.append(usuario.username)
#         lista_usuario.append(usuario.email)
#
#     print(lista_usuario)
#
#
# with app.app_context():
#     usuario = Usuario.query.filter_by(username="Marcelo").first()
#     print(usuario)
#     print(usuario.id)
#     print(usuario.username)
#     print(usuario.email)

# with app.app_context():
#     post = Post(titulo='Post 1', corpo='Post 1', id_usuario=1)
#     database.session.add(post)
#     database.session.commit()


# with app.app_context():
#     posts = Post.query.all()
#     print(posts)
#     for post in posts:
#         print(post.autor.id)
#         print(post.autor.username)
#         print(post.autor.email)
#         print(post.id)
#         print(post.titulo)
#         print(post.corpo)
#         print(post.data_criacao)


with app.app_context():
    database.drop_all()
    database.create_all()
