"""
Initialise
    Takes Config's URI info
    configures the Flask app to simply the db instance
    applies it to the Flask app
"""


class Initialise:
    def db(self, app):
        app.config.from_object("website.config.Config")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(
            app.config["DB_USERNAME"],
            app.config["DB_PASSWORD"],
            app.config["DB_LOCATION"],
            app.config["DB_DATABASE"]
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SECRET_KEY'] = 'password'
        return app
