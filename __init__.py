from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # import for database usage
from os import path
from flask_login import LoginManager  # helps to manage all login required things

# the __init__.py file makes the website file a python package in the directory

db = SQLAlchemy()  # define a new database.. this is an object
DB_NAME = "database.db"  # new database name


def create_app():
    app = Flask(__name__)  # initialize the Flask app
    app.config['SECRET_KEY'] = 'kggkdk kkgffk'  # encrypts the cookie data -- the key is the password for the site
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # tells flask we have a db and where its located
    db.init_app(app)  # initializes the db and tells flask this is the app used for the db

    from .views import views  # tells flask we have some blueprints for our application
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  # registers the blueprints with the flask app
    app.register_blueprint(auth, url_prefix='/')  # url tells where to access all the blueprints pages within the url

    from .models import User, Note  # it is .model b/c it is a relative import
    # above ensures that model.py runs before we initialize the db
    # defines the classes in model.py

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # location flask redirects if user isn't logged in
    login_manager.init_app(app)  # tells manager which app we are using

    @login_manager.user_loader  # tells flask how to load a user
    def load_user(id):
        return User.query.get(int(id))  # looks for the primary key (id)

    return app
