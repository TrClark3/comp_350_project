from initialise import Initialise
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

app = Flask(__name__)
init = Initialise()
app = init.db(app)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
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


db.create_all()


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'password', 'f_name', 'l_name', 'age')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

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

        user = User(username,password,first_name,last_name,age)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {first_name} {last_name} inserted.'
        })

    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            return jsonify({ 'Message': 'Must provide the user ID'})

        user = User.query.get(id)
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
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(id)} deleted.'
        })


api.add_resource(UserManager, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)