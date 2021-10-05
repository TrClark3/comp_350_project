from flask import Blueprint, render_template, request, redirect, url_for

from website import db
from website.models import User
import json

views = Blueprint('views', __name__)

# Homepage. Uses index.html
@views.route('/home')
@views.route('/')
def home():
    title = "Home"
    return render_template('index.html', title=title)

# SignUp Page. Uses signUp.html
@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    title = "Sign Up"
    # Handles POST method logic
    if request.method == 'POST':
        # collect form data, NOTE: age is odd to query in this context, should we consider deleting?
        f_name = request.form.get('firstname')
        l_name = request.form.get('lastname')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        new_user = User(username=username, password=password1,
                        first=f_name, last=l_name, age=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.thanks'))

    # Render the sign-up page
    return render_template('sign-up.html', title=title)

@views.route('/thanks')
def thanks():
    title = "Thank you!"
    return render_template('thanks.html', title=title)

# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():
    title = "Log In"
    return render_template('login.html', title=title)