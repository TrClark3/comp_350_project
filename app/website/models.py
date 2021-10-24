from website import db, ma, login_manager
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin


# Models
class User(UserMixin, db.Model):
    # Structure
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    f_name = db.Column(db.String(32))
    l_name = db.Column(db.String(32))
    age = db.Column(db.Integer) 
    # (NOTE) Age should probably be swapped out with an email field. Thoughts? - Travis

    def get_id(self):
        return (self.user_id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __init__(self, username, password, first, last, age):
        self.username = username
        self.password = password
        self.f_name = first
        self.l_name = last
        self.age = age
#Login Form Model for existing Usersused in views.log_in route)
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    remember = BooleanField('Remember me')

#SignUp Form Model for new Users (used in views.sign_up route)
class SignUpForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])
    f_name = StringField('first name', validators=[InputRequired(), Length(min=2, max=32)])
    l_name = StringField('last name', validators=[InputRequired(), Length(min=2, max=32)])

class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))

    def __init__(self, firstname, lastname):
        self.f_name = firstname
        self.l_name = lastname


# Schema
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class EmployeesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
