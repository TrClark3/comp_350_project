from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import logging

from website import db
from website.models import User, HotelReservation, Customer, Employee, HotelRoom
from website.models import user_schema, users_schema, rooms_schema, customer_schema


def dummy_data():
    objects = [
        User(username="JSmith1", password="jonnyboy", first="John", last="Smith", age=33),
        User(username="GDylan", password="spa4321", first="George", last="Dylan", age=53),
        User(username="AliceInWonderland", password="alice_spa123", first="Alice", last="Anston",
             age=32),
        User(username="JeffRedd", password="reddingJEFF39", first="Jeffrey", last="Redding", age=39),
        User(username="ImKyle", password="IMtheREALkyle", first="Kyle", last="Hirokai-Berman",
             age=28),
        User(username="Brayden23", password="brayd_spa23", first="Brayden", last="Daniels", age=23),
        User(username="BevSpa", password="bevspa_64", first="Beverly", last="Jacobs", age=64),
        User(username="JennyR", password="jenspa_34", first="Jennifer", last="Cherry", age=34),
        User(username="gaben", password="valve$$$", first="Gabe", last="Newell", age=59),

        Employee(firstname="Morgan", lastname="Greensburough"),
        Employee(firstname="Tim", lastname="Heidecker"),
        Employee(firstname="Eric", lastname="Wareheim"),
        Employee(firstname="Bruce", lastname="Floyd"),
        Employee(firstname="Hassan", lastname="Abrahim"),
        Employee(firstname="Jackson", lastname="Tucker"),
        Employee(firstname="Shawn", lastname="Goodwin"),
        Employee(firstname="Ria", lastname="Rodrigez"),
        Employee(firstname="Sienna", lastname="Anderson"),
        Employee(firstname="Hazel", lastname="Stanton"),
        Employee(firstname="Irene", lastname="Morrison"),
        Employee(firstname="Yasmin", lastname="Price"),

        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=0),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="JUNIOR", smoking=1),
        HotelRoom(type="QUEEN", smoking=0),
        HotelRoom(type="QUEEN", smoking=0),
        HotelRoom(type="QUEEN", smoking=0),
        HotelRoom(type="QUEEN", smoking=0),
        HotelRoom(type="QUEEN", smoking=0),
        HotelRoom(type="QUEEN", smoking=1),
        HotelRoom(type="QUEEN", smoking=1),
        HotelRoom(type="QUEEN", smoking=1),
        HotelRoom(type="QUEEN", smoking=1),
        HotelRoom(type="QUEEN", smoking=1),
        HotelRoom(type="KING", smoking=0),
        HotelRoom(type="KING", smoking=0),
        HotelRoom(type="KING", smoking=0),
        HotelRoom(type="KING", smoking=1),
        HotelRoom(type="KING", smoking=1),
        HotelRoom(type="KING", smoking=1)
    ]

    for obj in objects:
        db.session.add(obj)
        db.session.flush()

    db.session.commit()


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


def get_reservations():
    reservations = HotelReservation.query.all()
    dump = rooms_schema.dump(reservations)
    return jsonify(dump), 200


def get_reservation(in_date, out_date):
    return None


def delete_reservation():
    return None


@roomApi.route('/rooms/add', methods=['POST'])
def make_reservation():

    return None
