from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from website import db
from website.models import *
import json

views = Blueprint('views', __name__)


# Homepage. Uses index.html
@views.route('/home')
@views.route('/')
def home():
    return render_template('index.html')


# SignUp Page. Uses sign-up.html
@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # Create form from SignUpForm class in models.py
    form = SignUpForm()

    # Holds possible error message during sign up process
    error = None

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # Create new user from form data
        new_user = User(username=form.username.data, password=hashed_password, first=form.f_name.data,
                        last=form.l_name.data, age=0)
        
        # Add user to database, if username doesn't already exist
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.thanks'))
        except IntegrityError:
            db.session.rollback()
            error = 'Username already taken!'

    return render_template('sign-up.html', form=form, error=error)


# TODO: view open rooms in time period
# @views.route('/reservations', methods=['GET', 'POST'])
# def reservation():
#     form = ReservationSearchForm()
#     error = None
#     rooms = None
#
#     if form.validate_on_submit():
#         rooms = HotelReservation.query.filter_by(check_in=form.start_date.data, check_out=form.end_date.data).all()
#
#     return render_template('reservations.html', form=form, error=error, rooms_available=rooms)


# TODO: reserve a room
@views.route('/reservations/make', methods=['GET', 'POST'])
def make_reservation():
    form = ReservationForm()
    error = None

    if form.validate_on_submit():
        user = Customer(username=form.username.data, password=generate_password_hash(form.password.data),
                        ptype=form.payment_type.data, pinfo=form.payment_info.data)

    return render_template('create-reservation.html', form=form, error=error)

# Sign up completed successfully. Uses thanks.html
@views.route('/thanks')
def thanks():
    return render_template('thanks.html')


# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():

    # Create form from LoginForm clasee in models.py
    form = LoginForm()
    # Holds possible error message during log in process
    error = None

    if form.validate_on_submit():

        # Find user via username in database and confirm hashed password
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('views.user_dashboard'))
            
        error = "Username or password is incorrect. Please try again."
            
    return render_template('login.html', form=form, error=error)


# User's dashboard page. Uses user-dashboard.html
@views.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user-dashboard.html', user=current_user.username, name=current_user.f_name)


# User log out, redirects to homepage (index.html)
@views.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('views.home'))