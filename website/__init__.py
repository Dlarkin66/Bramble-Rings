from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from . import secret
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = "database.db" 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51N6HKxLW7Q4gXOtz84S5EXWUIXk3tVHvjMrxACoWQMCtT6b3J9DErPDR9EemqkDiJllTXomaEKMkmRMf4i11bu2900M3k3YXi1"
    app.config['STRIPE_SECRET_KEY'] = secret.stripe_secret_key
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'brambleringshelp@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jfyvdvyzfirsjmvf'

    mail = Mail(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

