from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "2c004d6e250bae0f82d5ad8e975d4566"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "É necessario fazer login ou criar uma conta para acessar a pagina"
login_manager.login_message_category = "alert-info"

#o main.py esta será o arquivo de execução iunicial.
#no main.py chama o __init__.py
#o __init__.py so coloca o site no ar
#então depois que colocar o site no ar tem que chamar as rotas
#no caso a linha abaixo
#por isso esse importe esta depois da criação do APP
#pois as rotas precisa do APP para rodar
from comunidade import routes