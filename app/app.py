from flask.templating import render_template
from initialise import Initialise
from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

# Initialization
app = Flask(__name__)

# create db URI and pass through
init = Initialise()
app = init.db(app)

# Init listener, sql functionality, and modeling schema
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
        first_name = request.form['firstname']
        last_name = request.form['lastname']

        return redirect(url_for('thanks'))

    # Render the sign-up page
    return render_template('sign-up.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

# create db structures
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    f_name = db.Column(db.String(32))
    l_name = db.Column(db.String(32))
    age = db.Column(db.Integer)

    def __init__(self, username, password, first, last, age):
        self.username = username
        self.password = password
        self.f_name = first
        self.l_name = last
        self.age = age


# Uses Models to run create tables in database
db.create_all()


# allows for easy JSON and HATEOAS strucutre
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


# Api (GET, POST, PUT, DELETE) pertaining to Users
# Each method takes care of validation
class UserManager(Resource):
    @staticmethod
    def get():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            users = User.query.all()
            return jsonify(users_schema.dump(users))
        user = User.query.get(user_id)
        return jsonify(user_schema.dump(user))

    @staticmethod
    def post():
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['f_name']
        last_name = request.json['l_name']
        age = request.json['age']

        user = User(username, password, first_name, last_name, age)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {first_name} {last_name} inserted.'
        })

    @staticmethod
    def put():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = User.query.get(user_id)
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['f_name']
        last_name = request.json['l_name']
        age = request.json['age']

        user.username = username
        user.password = password
        user.f_name = first_name
        user.l_name = last_name
        user.age = age

        db.session.commit()
        return jsonify({
            'Message': f'User {first_name} {last_name} altered'
        })

    @staticmethod
    def delete():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(user_id)} deleted.'
        })


# Links the whole UserManager class (all of its methods to the url /api/users
api.add_resource(UserManager, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)
