
import email
from hashlib import sha256
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    # data = request.form  # Access the form attribute of the POST request
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first() # Return first user with specified email

        if user:
            if check_password_hash(user.password, password=password):
                flash("Logged in Successfully!", category='success')
                login_user(user=user, remember=True) # Create session by using remember=True

                return redirect(url_for('views.home')) # Redirect user to home page
            else:
                flash("password is incorrect, try again", category='error')
        else:
            flash("User does not exist")

    return render_template('login.html', user=current_user) # Pass current_user context to see if user is authenticated (Cookie exists)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # Return user to login page

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_exists = User.query.filter_by(email=email).first() # Check if user already exists with this email

        if user_exists:
            flash("A user with the email specified already exists, please use a different email", category='error')
        elif not "@" in str(email) and len(email) < 5:
            flash("Email must contain @ and be longer than 4 characters", category='error')
        elif len(first_name) < 2:
            flash("First name must be longer than 1 characters", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match", category='error')
        elif len(password1) < 7:
            flash("Password must be 7 or more characters", category='error')
        else:
            # Create new User
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password=password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(user=new_user, remember=True) # Create session by using remember=True
            return redirect(url_for('views.home'))
            
    return render_template('sign_up.html', user=current_user)