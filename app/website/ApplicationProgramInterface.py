from flask import Blueprint, request, jsonify

from website import db
from website.models import User, user_schema, users_schema

userApi = Blueprint('userApi', __name__)


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
