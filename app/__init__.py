from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

from app.controllers import routes  # Importe as rotas após inicializar o app e as extensões

from app.models.models import User  # Importe o modelo de usuário

@login_manager.user_loader
def load_user(user_id):
    # Esta função é necessária para que o Flask-Login saiba como carregar um usuário
    return User.query.get(int(user_id))



