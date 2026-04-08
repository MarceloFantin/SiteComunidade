from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, length, email, equal_to, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user



#aqui tem que criar os formularios que vai aparecer nas paginas HTML
#usando o FlasForm que ja esta pronto no flask
#e o wtfform que tem os tipos dos campos
#antes tem que instalar pip install flask-wtf
class FormCriarConta(FlaskForm):
    username = StringField("Nome do Usuario", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), email()])
    senha = PasswordField("Senha", validators=[DataRequired(), length(6, 20)])
    confirmacao = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_submit_criarconta = SubmitField("Criar Conta")

    #para criar uma validação aqui dentro do form obrigatoriamente a a função tem que começar com
    #a nome validade_ isso é uma funcionalidade do flask
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(f"E-mail {email.data} ja cadastrado. Cadastre-se com outro email ou faça login")


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), email()])
    senha = PasswordField("Senha", validators=[DataRequired(), length(6, 20)])
    lembrar_dados = BooleanField("Lembrar dados de Acesso")
    botao_submit_login = SubmitField("Fazer Login")

class FormEditarPerfil(FlaskForm):
    username = StringField("Nome do Usuario", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), email()])
    foto_perfil = FileField("Atalizar Foto do Perfil", validators=[FileAllowed(["jpeg","jpg", "png"])])

    curso_execel = BooleanField("Excel")
    curso_vba = BooleanField("VBA")
    curso_Powerbi = BooleanField("Power BI")
    curso_python = BooleanField("Python")
    curso_ppt = BooleanField("Apresentações")
    curso_sql = BooleanField("SQL")


    botao_submit_editarperfil = SubmitField("Confimar Edição")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(f"E-mail {email.data} ja cadastrado para outro usuario. Cadastre com outro email ")



class FormCriarPost(FlaskForm):
    titulo = StringField("Titulo do Post", validators=[DataRequired(), length(2, 140)])
    corpo = TextAreaField("Escreva seu post aqui", validators=[DataRequired()])
    botao_submit_criarpost = SubmitField("Criar Post")
