from flask import render_template, request, redirect, flash, url_for, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets, os



@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()) #Query em ordem decrescente pros pots novos subir na página
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next') #Pega o valor de um parâmetro (args) de url especifico
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login, e-mail ou senha inválidos', 'alert-danger')
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        #Criando a instancia do usuário e passando os parâmetros a partir do form_criarconta que esta na página do site
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com suceso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    #Usando url_for para navegar no diretório fotos_perfil e passando o nome do arquivo como uma variável chamanto o atributo da classe Usuario dentro do arquivo models
    return render_template('perfil.html', foto_perfil=foto_perfil)
    #passando a variável foto perfil como argumento para ser acessado na página /perfil


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

#Meio merda, usar salvar_imagem2(), tá bem melhor
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    #alterando nome do arquivo para impedir que sobreponha arquivos com o mesmo nome
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    #criando o caminho com o novo nome do arquivo para salvar
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    #reduzindo o tamanho da imagem
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


#function melhorada pra evitar inflar o banco de dados com img (posteriormente criar um sistema de id de usuário com uma constante p/ aprimorar isso)
def salvar_imagem2(imagem):
    nome, extensao = os.path.splitext(imagem.filename)
    nome_usuario = current_user.email
    nome_arquivo = nome_usuario + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


#Function para percorrer o html e salvar em uma lista e ao fim dar join pra converter em uma string p/ armazenar no banco de dados
def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name: 
            if campo.data: #campo foi validado
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    form = FormEditarPerfil()
    #Instanciando o objeto FormEditarPerfil do arquivo forms.py para criar formulários dentro da página
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem2(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    #validate_on_submit automaticamente executa as funções que começam com validate_ da classe no arquivo forms.py
    #Atualizando o banco de dados com os novos dados preenchidos no form
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    #Preenchendo o campo vazio automaticamente quando der um GET na página
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)