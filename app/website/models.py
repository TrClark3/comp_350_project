from flask import app, url_for, redirect, Blueprint
from flask_login.mixins import AnonymousUserMixin
from werkzeug.exceptions import abort
from website import db, ma, login_manager, admin, views
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, DateField, SelectField, RadioField, TimeField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
import enum


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
class User(UserMixin, db.Model):
    __tablename__ = "user"

    # Structure
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    f_name = db.Column(db.String(32))
    l_name = db.Column(db.String(32))
    payment_type = db.Column(db.Enum(PaymentType), default="CASH")
    payment_info = db.Column(db.String(50), default="0")
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.user_id

    # Return user id of logged in user for current session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __init__(self, username, password, first, last, pay_type, pay_info, is_admin):
        self.username = username
        self.password = password
        self.f_name = first
        self.l_name = last
        self.payment_type = pay_type
        self.payment_info = pay_info
        self.is_admin = is_admin


# Specifies properties for unsigned in Users
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.is_admin= False


login_manager.anonymous_user = Anonymous


class Employee(db.Model):
    __tablename__ = "employee"

    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=True)

    def __init__(self, firstname, lastname, is_admin):
        self.f_name = firstname
        self.l_name = lastname
        self.is_admin = is_admin


class HotelRoom(db.Model):
    __tablename__ = "hotelroom"

    room_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_type = db.Column(db.Enum(RoomType))
    smoking = db.Column(db.Boolean, default=0, nullable=False)

    def __init__(self, number, type, smoking):
        self.room_num = number
        self.room_type = type
        self.smoking = smoking


class HotelReservation(db.Model):
    __tablename__ = "hotelreservation"

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_num = db.Column(db.Integer)
    cust_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)

    def __init__(self, room_num, cust_id, check_in, check_out):
        self.room_num = room_num
        self.cust_id = cust_id
        self.check_in = check_in
        self.check_out = check_out


class SpaService(db.Model):
    __tablename__ = "spaservice"

    service_type = db.Column(db.Enum(ServiceType), primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self, service_type, start_time, end_time):
        self.service_type = service_type
        self.start_time = start_time
        self.end_time = end_time


class SpaReservation(db.Model):
    __tablename__ = "spareservation"

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_num = db.Column(db.Integer, db.ForeignKey('hotelreservation.res_id'))
    cust_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    spa_start = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    service_type = db.Column(db.Enum(ServiceType), db.ForeignKey('spaservice.service_type'))

    def __init__(self, room_num, cust_id, spa_start, start_time, end_time, service_type):
        self.room_num = room_num
        self.cust_id = cust_id
        self.spa_start = spa_start
        self.start_time = start_time
        self.end_time = end_time
        self.service_type = service_type


# Schema
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class EmployeesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
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


# Admin Model View
class AdminModelView(ModelView):

    # Check if user is admin. Only one user should have this privledge
    # Admin then has right to add employee objects with same privledge
    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated
        else:
            abort(401)


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Employee, db.session))
admin.add_view(AdminModelView(HotelReservation, db.session))
admin.add_view(AdminModelView(HotelRoom, db.session))
admin.add_view(AdminModelView(SpaReservation, db.session))
admin.add_view(AdminModelView(SpaService, db.session))

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
rooms_schema = HotelReservationSchema(many=True)
services_schema = SpaServiceSchema(many=True)


# Login Form Model for existing Usersused in views.log_in route)
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    remember = BooleanField('Remember me')


# SignUp Form Model for new Users (used in views.sign_up route)
class SignUpForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    f_name = StringField('first name', validators=[InputRequired(), Length(min=2, max=32)])
    l_name = StringField('last name', validators=[InputRequired(), Length(min=2, max=32)])


class ReservationForm(FlaskForm):
    room_type = SelectField('Room Type', choices=[('KING', 'King'), ('QUEEN', 'Queen'), ('JUNIOR', 'Junior')])
    smoking = BooleanField('Smoking')
    start_date = DateField('start date', validators=[InputRequired()])
    end_date = DateField('end date', validators=[InputRequired()])

class SpaReservationForm(FlaskForm):
    # Bath Services (Cost: $2.50/min)
    service1 = RadioField('Mineral Bath', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')

    # Massage Services (Cost: $2.00/min)
    service2a = RadioField('Swedish Message', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')
    service2b = RadioField('Shiatsu Message', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')
    service2c = RadioField('Deep Tissue Message', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')

    # Specialty Services (Cost: $3.50/min)
    service3a = RadioField('Hot Stone', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')
    service3b = RadioField('Sugar Scrub', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')
    service3c = RadioField('Herbal Body Wrap', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')
    service3d = RadioField('Botanical Mud Wrap', choices=[('90', '90 minutes'), ('60', '60 minutes'), ('0', 'Neither')], default='0')

    day = DateField('Choose Day', validators=[InputRequired()])
    time = TimeField('Choose Time', validators=[InputRequired()])
    
class ReservationSearchForm(FlaskForm):
    start_date = DateField('start date', validators=[InputRequired()])
    end_date = DateField('end date', validators=[InputRequired()])


class AdminSignUpForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])

