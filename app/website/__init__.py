from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    # Sets up DB & Configs
    from website.initialise import Initialise
    init = Initialise()
    app = init.db(app)

    ma.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from .views import views
    from website.ApplicationProgramInterface import userApi, dummy_data

    app.register_blueprint(userApi, url_prefix='/api')
    app.register_blueprint(views, url_prefix='/')

    db.create_all(app=app)
    dummy_data()

    return app
