from flask import Blueprint, render_template, request, redirect, url_for

from website import db
from website.models import User
import json

views = Blueprint('views', __name__)

# Homepage. Uses index.html
@views.route('/home')
@views.route('/')
def home():
    return render_template('index.html')

# SignUp Page. Uses signUp.html
@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Handles POST method logic
    if request.method == 'POST':
        # collect form data, NOTE: age is odd to query in this context, should we consider deleting?
        f_name = request.form.get('firstname')
        l_name = request.form.get('lastname')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Verify all form fields filled out, if not rerender sign-up, carrying over filled out fields (except password)
        if not f_name or not l_name or not username or not password1 or not password2:
            error_statement = "Please fill out all form fields."
            return render_template('sign-up.html', error_statement=error_statement, f_name=f_name,
                l_name=l_name,
                username=username)

        # create new User
        new_user = User(username=username, password=password1,
                        first=f_name, last=l_name, age=0)
        # Push to database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.thanks'))
        except:
            return "An error occured during sign up process..."

    else:
        # Render the sign-up page
        return render_template('sign-up.html')

@views.route('/thanks')
def thanks():
    return render_template('thanks.html')

# Login Page. Uses login.html
@views.route('/log-in', methods=['GET', 'POST'])
def log_in():
    return render_template('login.html')