import click
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)
login = LoginManager(flask_app)
login.login_view = 'admin_login'

from app import routes, models, errors


@click.command(name='create_admin')
@with_appcontext
def create_admin():
	admin = models.User(email=flask_app.config['ADMIN_EMAIL'],
						password=flask_app.config['ADMIN_PASSWORD'])
	admin.password = generate_password_hash(admin.password, 'sha256', salt_length=12)
	db.session.add(admin)
	db.session.commit()

flask_app.cli.add_command(create_admin)
