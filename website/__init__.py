from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os
from os import path

db = SQLAlchemy()
DB_NAME = "database.db" 


def create_app():
    # App configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['STRIPE_PUBLIC_KEY'] = "pk_live_51N6HKxLW7Q4gXOtz6rxys8vMr1VSjaIE8dbVrroot5HFOFyZQJVpnlL5hZidkoBDo4WHhcNP8eBx63VNdSFoylke00WbbE7t1x"
    app.config['STRIPE_SECRET_KEY'] =  os.environ.get('STRIPE_SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_SECRET_KEY')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    mail = Mail(app)

    # Import views and authentification blueprints
    from .views import views
    from .auth import auth
    from .models import User

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Load user for login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Create the database if it doesn't exist
    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')



