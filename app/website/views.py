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
    is_logged_in = current_user.is_authenticated
    return render_template('index.html', user=current_user.username, is_logged_in = is_logged_in)


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
        new_user = User(username=form.username.data, password=hashed_password,
                        first=form.f_name.data, last=form.l_name.data, pay_type="CASH", pay_info="0", is_admin=False)

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
# NOTE: We should require login here and maybe not add a new customer session to the db? -Travis
@views.route('/reservations/make', methods=['GET', 'POST'])
def make_reservation():
    form = ReservationForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        ptype = form.payment_type.data
        pinfo = form.payment_info.data

        # TODO: fix bug where it creats multiple customers
        # might be password hashes not matching causing it to make a new customer
        cust = User.query.filter_by(username=username, password=password).all()
        if not cust:
            cust = User(username, password, ptype, pinfo)
            db.session.add(cust)
            db.session.commit()

        room = HotelRoom.query.filter_by(room_type=form.room_type.data, smoking=form.smoking.data).first()
        if room:
            reservation = HotelReservation.query.filter_by(check_in=form.start_date.data,
                                                           check_out=form.end_date.data).all()
            if not reservation:
                reservation = HotelReservation(room_num=room.room_num, user_id=cust.user_id,
                                               check_in=form.start_date.data, check_out=form.end_date.data)
                db.session.add(reservation)
                db.session.commit()
                return redirect(url_for('views.thanks'))
            else:
                # TODO: more info on the error messages
                error = "A reservation is already made"

        else:
            error = "Room selected Is not available. Choose another."

    return render_template('create-reservation.html', user=current_user.username, form=form, error=error)


# Sign up completed successfully. Uses thanks.html
@views.route('/thanks')
def thanks():
    is_logged_in = current_user.is_authenticated
    return render_template('thanks.html', user=current_user.username, is_logged_in = is_logged_in)


# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():

    # Create form from LoginForm class in models.py
    form = LoginForm()
    # Holds possible error message during log in process
    errors = None

    if form.validate_on_submit():

        # Find user via username in database and confirm hashed password
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('views.user_dashboard'))
            
        errors = "Username or password is incorrect. Please try again."
            
    return render_template('login.html', form=form, error=errors)


# User's dashboard page. Uses user-dashboard.html
@views.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user-dashboard.html', user=current_user.username, name=current_user.f_name)


@views.route('/services')
def services():
    is_logged_in = current_user.is_authenticated
    return render_template('services.html', user=current_user.username, is_logged_in = is_logged_in)


@views.route('/book-services', methods=['GET', 'POST'])
@login_required
def book_services():

    form = SpaReservationForm()

    error = None

    if form.validate_on_submit():

        # If total minutes of services exceeds 300 minutes or is 0 throw error. I'm aware of how terribly this is implemented lol ;(
        if (int(form.service1.data) + int(form.service2a.data) + int(form.service2b.data)
        + int(form.service2c.data) + int(form.service3a.data) + int(form.service3b.data) + int(form.service3c.data) + int(form.service3d.data)) > 300:

            error = 'Services booked cannot exceed 300 minutes in one day, please book additional services for next available day!'

        elif (int(form.service1.data) + int(form.service2a.data) + int(form.service2b.data)
        + int(form.service2c.data) + int(form.service3a.data) + int(form.service3b.data) + int(form.service3c.data) + int(form.service3d.data)) == 0:

            error = 'Please choose a service to continue with booking.'

        else:
            return redirect(url_for('views.thanks'))
            

    return render_template('book-services.html', user=current_user.username, form=form, error=error)


@views.route('/information')
def information():
    is_logged_in = current_user.is_authenticated
    return render_template('information.html', user=current_user.username, is_logged_in = is_logged_in)


# User log out, redirects to homepage (index.html)
@views.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('views.home'))


# Admin Initialization (Step 1/2)
@views.route('/admin-initialization', methods=['GET', 'POST'])
def admin_init():
    # Uses AdminSignUpForm in Models.py
    form = AdminSignUpForm()
    # Holds possible error message during authorization process
    error = None

    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "password":
            admin_user = User(username='admin', password="password", first="root", last="root",
            pay_type="CASH", pay_info="0", is_admin=True)
            # Add admin user to database, if it doesn't already exist
            try:
                db.session.add(admin_user)
                db.session.commit()
                flash('Admin account created. Please log in below.', 'success')
                return redirect(url_for('views.admin_login'))
            except IntegrityError:
                db.session.rollback()
                flash('Admin account already created. Please log in below.', 'warning')
                return redirect(url_for('views.admin_login'))
        else:
            error = "Wrong admin credentials."
            
    return render_template('admin/admin-init.html', form=form, error=error)


# Admin login (Step 2/2)
@views.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    # Create form from LoginForm class in models.py
    form = LoginForm()
    # Holds possible error message during log in process
    error = None

    if form.validate_on_submit():

        # Checks if correct credentials provided & if admin account created yet.
        if form.username.data == "admin" and form.password.data == "password":
            admin = User.query.filter_by(username=form.username.data).first()

            if admin:
                login_user(admin)
                return redirect(url_for('views.admin_home'))
            flash("Admin account not yet created. Please perform Admin Initialization step first.", "warning")    
            return redirect(url_for('views.admin_login'))

        else:
            error = "Wrong admin credentials."
            
    return render_template('admin/admin-login.html', form=form, error=error)

@views.route('/admin')
@login_required
def admin_home():
    return redirect(url_for('admin.index'))

@views.route('/view-reservations')
@login_required
def view_reservations():
    return render_template('view-reservations.html', user=current_user.username)