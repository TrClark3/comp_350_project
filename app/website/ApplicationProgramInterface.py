from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import logging

from website import db
from website.models import User, user_schema, users_schema, HotelReservation, rooms_schema

userApi = Blueprint('userApi', __name__)
roomApi = Blueprint('roomApi', __name__)


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


@userApi.route("/users/add", methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        username = request.args['username']
        password = request.args['password']
        f_name = request.args['f_name']
        l_name = request.args['l_name']
        age = request.args['age']

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'),
                        first=f_name, last=l_name, age=age)

        db.session.add(new_user)
        db.session.commit()
        return f"Success! User {username} added!", 200

    return "Wrong method type", 404


@userApi.route("/users/update/<int:user_id>", methods=['GET', 'PUT'])
def update_user(user_id):
    if request.method == "PUT":
        user = User.query.get(user_id)

        if user is not None:
            user.username = request.args['username']
            user.password = request.args['password']
            user.f_name = request.args['f_name']
            user.l_name = request.args['l_name']
            user.age = request.args['age']
            logging.getLogger('website').debug(user)

            db.session.commit()
            return f"Success! User {str(user_id)} changed!", 200

        return f"Failure! User {str(user_id)} not found!", 404

    return "Wrong method type", 404


@roomApi.route('/rooms', methods=['GET'])
def get_reservations():
    reservations = HotelReservation.query.all()
    dump = rooms_schema.dump(reservations)
    return jsonify(dump), 200


@roomApi.route('/room', methods=['GET'])
def get_reservation(in_date, out_date):
    reservations = HotelReservation.query.filter_by(check_in=in_date, check_out=out_date).all()

    dump = rooms_schema.dump(reservations)
    return jsonify(dump), 200


def delete_reservation():
    return None


@roomApi.route('/rooms/add', methods=['POST'])
def make_reservation():

    return None
