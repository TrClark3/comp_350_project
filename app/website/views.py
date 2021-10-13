from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


from website import db
from website.models import User, LoginForm, SignUpForm
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

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # Create new user from form data
        new_user = User(username=form.username.data, password=hashed_password, 
        first=form.f_name.data, last=form.l_name.data, age = 0)
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.thanks'))

    return render_template('sign-up.html', form=form)

# Sign up completed successfully. Uses thanks.html
@views.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():

    # Create form from LoginForm clasee in models.py
    form = LoginForm()

    if form.validate_on_submit():

        # Find user via username in database and confirm hashed password
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('views.user_dashboard'))
            
            return '<h2> That username or password combination is incorrect. Please try again. <h2>' # probs a cooler way to do this
            
    return render_template('login.html', form=form)

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