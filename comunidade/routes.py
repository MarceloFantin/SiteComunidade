from comunidade import app, database, bcrypt
from flask import render_template, redirect, request, url_for, flash, abort
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade.models import Usuario, Post
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("home.html", posts=posts)

@app.route('/contato')
def contato():
    return render_template("contato.html")

#@login_requered so vai deixar entrar na pagina se o usuariuo estiver logado
@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email: {form_login.email.data}', 'alert-success')
            #request.args traz um docionario com todos os paramentros da url
            # request.args.get('next') pega o paremetro que esta na url da pagina nesse caso o paramentro next
            #examplo de URL http://127.0.0.1:5000/login?next=%2Fusuarios
            #tudo o que esta depois do ? é paramentro
            #nesse casp p valor do paramentro next = /uruarios
            paramentro_next = request.args.get('next')
            if paramentro_next:
                return redirect(paramentro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login e-mail ou senha incorreta', 'alert-danger')


    if form_criarconta.validate_on_submit() and "botao_submit_criarconta" in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', "alert-success")
        return redirect(url_for('home'))


    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', "alert-success")
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template("perfil.html", foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    # adiciona um codigo aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    #separa o nome da exteção do arquivo
    nome, extencao =  os.path.splitext(imagem.filename)
    #junta tudo para criar o nome do arquivo
    nome_arquivo = nome + codigo + extencao
    caminho_completo = os.path.join(app.root_path, 'static','fotos_perfil' , nome_arquivo)
    print(app.root_path)
    print(caminho_completo)
    # reduzir o tamanho da imagem
    tamanho = (400,400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imgagem no na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_curso(form):
    lista_cursos = []

    for campo in form:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)

    if lista_cursos:
        return ";".join(lista_cursos)

    return ("Não informado")



@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()

    if form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        if form_editar_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            #mudar o campo foto_perfil do usuario para no novo nome de imagem
            current_user.foto_perfil = nome_imagem

        current_user.cursos = atualizar_curso(form_editar_perfil)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', "alert-success")
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editar_perfil.username.data = current_user.username
        form_editar_perfil.email.data = current_user.email

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template("editarperfil.html",
                           foto_perfil=foto_perfil,
                           form_editar_perfil=form_editar_perfil)

@app.route("/post/criar", methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data,
                    corpo=form_criar_post.corpo.data,
                    autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))

    return render_template("criarpost.html", form_criar_post=form_criar_post)


@app.route("/post/<post_id>", methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        form_editar_post = FormCriarPost()
        if request.method == "GET":
            form_editar_post.titulo.data = post.titulo
            form_editar_post.corpo.data = post.corpo
            form_editar_post.botao_submit_criarpost.label.text = "Salvar Post"
        elif form_editar_post.validate_on_submit():
            post.titulo = form_editar_post.titulo.data
            post.corpo = form_editar_post.corpo.data
            database.session.commit()
            flash(f'Post atualizado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form_editar_post = None

    return render_template("post.html", post=post, form_editar_post=form_editar_post)

@app.route("/post/<post_id>/excluir", methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post excluido com sucesso!", "alert-danger")
        return redirect(url_for('home'))
    else:
        abort(403)


