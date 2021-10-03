from flask import Blueprint, request, jsonify
from flask_restplus import Resource

from website import db
from website.models import User, user_schema, users_schema

userApi = Blueprint('userApi', __name__)


# @userApi.route('/users')
# class UserManager(Resource):
#     @staticmethod
#     def post():
#         username = request.json['username']
#         password = request.json['password']
#         first_name = request.json['f_name']
#         last_name = request.json['l_name']
#         age = request.json['age']
#
#         user = User(username, password, first_name, last_name, age)
#         db.session.add(user)
#         db.session.commit()
#
#         return jsonify({
#             'Message': f'User {first_name} {last_name} inserted.'
#         })
#
#     @staticmethod
#     def put():
#         try:
#             user_id = request.args['user_id']
#         except Exception as _:
#             user_id = None
#
#         if not user_id:
#             return jsonify({'Message': 'Must provide the user ID'})
#
#         user = User.query.get(user_id)
#         username = request.json['username']
#         password = request.json['password']
#         first_name = request.json['f_name']
#         last_name = request.json['l_name']
#         age = request.json['age']
#
#         user.username = username
#         user.password = password
#         user.f_name = first_name
#         user.l_name = last_name
#         user.age = age
#
#         db.session.commit()
#         return jsonify({
#             'Message': f'User {first_name} {last_name} altered'
#         })


@userApi.route("/users", methods=['GET'])
def all_users():
    us = User.query.all()
    dump = users_schema.dump(us)
    return jsonify(dump), 200


@userApi.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        dump = user_schema.dump(user)
        return jsonify(dump), 200

    return f"User {str(user_id)} does not exist!", 404


@userApi.route("/users/del/<int:user_id>", methods=['GET', 'DELETE'])
def delete_user(user_id):
    if request.method == "DELETE":
        user = User.query.get(user_id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return f"Success! User {str(user_id)} deleted!", 200

        return f"Failure! User {str(user_id)} does not exist!", 404

    return "DELETING", 200
