# auth is for login credentials

from flask import Blueprint
from flask import render_template  # to use an html template page
from flask import request  # to get information in a form
from flask import flash  # to display messages to the user
from .models import User  # to import a user so we can add a new user to db
from werkzeug.security import generate_password_hash, check_password_hash  # to hash the password
from flask import redirect
from flask import url_for
from . import db
from flask_login import login_user, login_required, logout_user, current_user, login_manager


auth = Blueprint('auth', __name__)  # sets up a blueprint for our flask application


@auth.route('/login', methods=['GET', 'POST'])  # webpage for the login -- add '/login' to end of url to see page
def login():
    # data = request.form  # to get information sent in the forms
    # print(data)

    if request.method == 'POST':  # if we are signed in
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # checks if user email is in the db, then returns first result
        if user:  # if we actually find a user
            if check_password_hash(user.password, password):  # checks if pw is same as the hashed pw on the server
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # this logs in the user and remembers they are logged in
                return redirect(url_for('views.home'))  # after login, redirects to homepage
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)  # place the html file for the page here
    # you can add variables or booleans after the coma above


@auth.route('/logout')
@login_required  # makes sure page can't be accessed without login first
def logout():
    logout_user()  # logs out the current user
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])  # GET loads the page up. POST is any change/addition to the page
def sign_up():
    if request.method == 'POST':  # if the request is a POST method (ex: submit button), it makes changes to DB etc/
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # input validation checks
        user = User.query.filter_by(email=email).first()  # checks if user email is in the db, then returns first result
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            # next line will display a message to the user
            # category= 'anything I want to create'
            flash("Email must be greater than 4 characters", category= 'error')
        elif len(firstName) < 2:
            flash('First name must be greater than 3 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            # creates a new user -- 'User' comes from model.py
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)  # this logs in the user and remembers they are logged in
            flash('Account Created!', category='success')
            # adds user to database
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


