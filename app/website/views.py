from re import A
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
        new_user = User(username=form.username.data, password=hashed_password,
                        first=form.f_name.data, last=form.l_name.data, age=0, is_admin=False)
        
        # Add user to database, if username doesn't already exist
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.thanks'))
        except IntegrityError:
            db.session.rollback()
            error = 'Username already taken!'

    return render_template('sign-up.html', form=form, error=error)


# Sign up completed successfully. Uses thanks.html
@views.route('/thanks')
def thanks():
    return render_template('thanks.html')


# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():

    # Create form from LoginForm class in models.py
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


@views.route('/services')
@login_required
def services():
    return render_template('services.html')


@views.route('/book-services')
@login_required
def book_services():
    return render_template('book-services.html')


@views.route('/information')
@login_required
def information():
    return render_template('information.html')


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
            admin_user = User(username='admin', password="password", first="root", last="root", age=100,
                              is_admin=True)
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
            
    return render_template('admin-init.html', form=form, error=error)


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
                return redirect(url_for('admin.index'))
            flash("Admin account not yet created. Please perform Admin Initialization step first.", "warning")    
            return redirect(url_for('views.admin_login'))

        else:
            error = "Wrong admin credentials."
            
    return render_template('admin-login.html', form=form, error=error)

