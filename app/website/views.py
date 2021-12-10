from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from website import db
from website.models import *

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

def check_dates(res_start, res_end, start, end):
    earliest_end = min(res_end, end)
    latest_start = max(res_start, start)
    overlap = (earliest_end - latest_start).days + 1
    return overlap  # + = overlap, 0 = same dates, - = no overlap


def check_room(reservations, room, start, end):
    for res in reservations:
        # compare dates
        no_overlap = (check_dates(res.check_in, res.check_out, start, end) < 0)
        # check room numbers
        diff_room = (res.room_num != room.room_num)

        if no_overlap or diff_room:
            return True

    return False


# TODO: reserve a room
@views.route('/reservations/make', methods=['GET', 'POST'])
def make_reservation():
    form = ReservationForm()
    error = None

    if form.validate_on_submit():
        room_type = form.room_type.data
        room_smoking = form.smoking.data
        date_start = form.start_date.data
        date_end = form.end_date.data
        r = None

        if date_start > date_end:  # Error dates are backward
            error = "Cannot Reserve a negative time period.\n"
        else:
            # Check all rooms by description
            rooms = HotelRoom.query.filter_by(room_type=room_type, smoking=room_smoking).all()

            # Joins and displays ALL HotelReservations with the Information of the Room
            # filtered by the room_type and if it is smoking or not
            reservations_made = HotelReservation.query.all()

            if reservations_made:  # There are reservations
                for room in rooms:
                    if check_room(reservations_made, room, date_start, date_end):
                        r = room
                        break

                if r is None:
                    error = 'The room type selected is not available in that time period'
            else:  # No Reservations
                r = rooms[0]

        if not error:  # No errors and a room is selected
            # make the reservation
            res = HotelReservation(r.room_num, current_user.user_id, date_start, date_end)
            db.session.add(res)
            db.session.commit()
            return render_template('reservation-confirmation.html', reservation=res)

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



@views.route('/book-services')
@login_required
def book_services():
    return render_template('book-services.html', user=current_user.username)


@views.route('/information')
def information():
    is_logged_in = current_user.is_authenticated
    return render_template('information.html', user=current_user.username, is_logged_in = is_logged_in)

@views.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

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