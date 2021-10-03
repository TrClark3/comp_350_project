from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

from website import db
from website.models import User
import json

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


# Handle a User Sign-Up
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

        # validate form data to fit in database. Commented out bc I need to import bootstrap but im too lazy rn
        # We should also validate the username is unique somehow
        """
            Technically since usernames are always unique in our database 
            we would need to handle the case if the entered username is already 
            in the database
                        - Alessasndro
        """

        # if (len(f_name) < 2 or len(f_name) > 32):
        #     flash('First Name must be between 2 and 32 characters.', category='error')
        # elif (len(l_name) < 2 or len(l_name) > 32):
        #     flash('Last Name must be between 2 and 32 characters.', category='error')
        # elif (len(username) < 4 or len(username) > 50):
        #     flash('Username must be between 4 and 50 characters.', category='error')
        # elif password1 != password2:
        #     flash('Passwords do not match!', category='error')
        # elif len(password1) < 5:
        #     flash('Password must be between 5 and 32 characters.', category='error')
        # else:
        #     # add user to database
        #     flash('Account Created!', category='success')

        # add user to database, encrypt password using werkzeug import
        new_user = User(username=username, password=generate_password_hash(password1, method='sha256'),
                        first=f_name, last=l_name, age=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.thanks'))

    # Render the sign-up page
    return render_template('sign-up.html')


@views.route('/thanks')
def thanks():
    return render_template('thanks.html')
