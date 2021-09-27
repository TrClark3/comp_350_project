from initialise import Initialise
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

# Initialization
app = Flask(__name__)

# create db URI and pass through
init = Initialise()
app = init.db(app)

# Init listener, sql functionality, and modeling schema
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def index():
    return render_template('index.html')

# Handle a User Sign-Up
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #Handles POST method logic
    if request.method == 'POST':

        #collect form data, NOTE: age is odd to query in this context, should we consider deleting?
        f_name = request.form.get('firstname')
        l_name = request.form.get('lastname')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #validate form data to fit in database. Commented out bc I need to import bootstrap but im too lazy rn
        #We should also validate the username is unique somehow

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
        new_user = User(f_name=f_name, l_name=l_name, username=username,
                    password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('thanks'))

    # Render the sign-up page
    return render_template('sign-up.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

# create db structures
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    f_name = db.Column(db.String(32))
    l_name = db.Column(db.String(32))
    age = db.Column(db.Integer)

    def __init__(self, username, password, first, last, age):
        self.username = username
        self.password = password
        self.f_name = first
        self.l_name = last
        self.age = age


# Uses Models to run create tables in database
db.create_all()


# allows for easy JSON and HATEOAS strucutre
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


# Api (GET, POST, PUT, DELETE) pertaining to Users
# Each method takes care of validation
class UserManager(Resource):
    @staticmethod
    def get():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            users = User.query.all()
            return jsonify(users_schema.dump(users))
        user = User.query.get(user_id)
        return jsonify(user_schema.dump(user))

    @staticmethod
    def post():
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['f_name']
        last_name = request.json['l_name']
        age = request.json['age']

        user = User(username, password, first_name, last_name, age)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {first_name} {last_name} inserted.'
        })

    @staticmethod
    def put():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = User.query.get(user_id)
        username = request.json['username']
        password = request.json['password']
        first_name = request.json['f_name']
        last_name = request.json['l_name']
        age = request.json['age']

        user.username = username
        user.password = password
        user.f_name = first_name
        user.l_name = last_name
        user.age = age

        db.session.commit()
        return jsonify({
            'Message': f'User {first_name} {last_name} altered'
        })

    @staticmethod
    def delete():
        try:
            user_id = request.args['user_id']
        except Exception as _:
            user_id = None

        if not user_id:
            return jsonify({'Message': 'Must provide the user ID'})

        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(user_id)} deleted.'
        })


# Links the whole UserManager class (all of its methods to the url /api/users
api.add_resource(UserManager, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)
