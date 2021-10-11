from flask import Blueprint, render_template, request, redirect, url_for
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash


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

    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password, 
        first=form.f_name.data, last=form.l_name.data, age = 100)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.thanks'))

    return render_template('sign-up.html', form=form)

# Sign up complete page. Uses thanks.html
@views.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():
    return render_template('login.html')