from comunidade import app, database
from comunidade.models import Usuario, Post

with app.app_context():
    database.drop_all()
    database.create_all()

#with app.app_context():
#    database.create_all()