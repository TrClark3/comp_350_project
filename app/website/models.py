import enum

from website import db, ma


# Enumerations
class PaymentType(enum.Enum):
    CC = "CC"
    CASH = "CASH"
    CHECK = "CHECK"


class ServiceType(enum.Enum):
    SERVICE1 = "SERVICE1"
    SERVICE2 = "SERVICE2"
    SERVICE3 = "SERVICE3"


class RoomType(enum.Enum):
    KING = "KING"
    QUEEN = "QUEEN"
    JUNIOR = "JUNIOR"


# Models
class User(db.Model):
    __tablename__ = "user"

    # Structure
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    f_name = db.Column(db.String(32))
    l_name = db.Column(db.String(32))
    age = db.Column(db.Integer)

    def __init__(self, username, password, first, last, age):
        self.username = username
        self.password = password
        self.f_name = first
        self.l_name = last
        self.age = age


class Employee(db.Model):
    __tablename__ = "employee"

    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))

    def __init__(self, firstname, lastname):
        self.f_name = firstname
        self.l_name = lastname


class Customer(db.Model):
    __tablename__ = "customer"

    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    payment_type = db.Column(db.Enum(PaymentType))
    payment_info = db.Column(db.String(50))

    def __init__(self, username, password, ptype, pinfo):
        self.username = username
        self.password = password
        self.payment_type = ptype
        self.payment_info = pinfo


class HotelRoom(db.Model):
    __tablename__ = "hotelroom"

    room_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_type = db.Column(db.Enum(RoomType))
    smoking = db.Column(db.Boolean)

    def __init__(self, number, type, smoking):
        self.room_num = number
        self.room_type = type
        self.smoking = smoking


class HotelReservation(db.Model):
    __tablename__ = "hotelreservation"

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_num = db.Column(db.Integer)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)


class SpaService(db.Model):
    __tablename__ = "spaservice"

    service_type = db.Column(db.Enum(ServiceType), primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


class SpaReservation(db.Model):
    __tablename__ = "spareservation"

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_num = db.Column(db.Integer, db.ForeignKey('hotelreservation.res_id'))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    spa_start = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    service_type = db.Column(db.Enum(ServiceType), db.ForeignKey('spaservice.service_type'))


# Schema
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class EmployeesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True


class HotelRoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HotelRoom
        include_fk = True


class HotelReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HotelReservation
        include_fk = True


class SpaServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpaService
        include_fk = True


class SpaReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpaReservation
        include_fk = True


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
