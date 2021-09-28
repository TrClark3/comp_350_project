from flask import request, jsonify
from flask_restful import Resource
from website import db
from website.models import User, user_schema, users_schema


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
