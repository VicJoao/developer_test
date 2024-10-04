from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models.models import Produto
from app.models.forms import ProdutoForm, LoginForm
from app.models.models import User

@app.route('/lista_produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user, form.password.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next_page = url_for('listar_produtos')
            return redirect(next_page)
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/produto/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        form.populate_obj(produto)
        db.session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('editar_produto.html', form=form)

@app.route('/produto/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

@app.route('/produto/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data
        )
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('novo_produto.html', form=form)

@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    # Verifique se o usuário já existe
    existing_user = User.query.filter_by(username='admin').first()
    if existing_user:
        return "O usuário admin já existe!"

    # Crie um novo usuário com a senha como um hash
    new_user = User(
        username='admin',
        email='admin@email.com'
    )
    new_user.set_password('admin')  # Define a senha como 'admin' e a armazena como um hash

    # Adicione o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return "Usuário admin criado com sucesso!"
