from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = "2c004d6e250bae0f82d5ad8e975d4566"

if os.getenv("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'comunidade.db')}"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "É necessario fazer login ou criar uma conta para acessar a pagina"
login_manager.login_message_category = "alert-info"

# Garante que a pasta instance exista para não dar erro de caminho
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

#verifica de o banco de dados esta criado
from comunidade import models
engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
inspetor = sqlalchemy.inspect(engine)
print(f"Tabelas encontradas: {inspetor.get_table_names()}")
if not inspetor.has_table("usuarios"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados Criada")
else:
    print("Base de ja existente dados")


#o main.py esta será o arquivo de execução iunicial.
#no main.py chama o __init__.py
#o __init__.py so coloca o site no ar
#então depois que colocar o site no ar tem que chamar as rotas
#no caso a linha abaixo
#por isso esse importe esta depois da criação do APP
#pois as rotas precisa do APP para rodar
from comunidade import routes