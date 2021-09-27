from .initialise import Initialise

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

db = SQLAlchemy()
ma = Marshmallow()
api = Api()


def create_app():
    app = Flask(__name__)

    # Sets up DB & Configs
    init = Initialise()
    app = init.db(app)

    api.init_app(app)
    ma.init_app(app)
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    db.create_all(app=app)

    return app
