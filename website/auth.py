
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    # data = request.form  # Access the form attribute of the POST request
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<p>Logout<p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if not "@" in str(email) and len(email) < 5:
            flash("Email must contain @ and be longer than 4 characters", category='error')
        elif len(firstName) < 2:
            flash("First name must be longer than 1 characters", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match", category='error')
        elif len(password1) < 7:
            flash("Password must be 7 or more characters", category='error')
        else:
            flash("Account created!", category="success")
            # Add user to database
    return render_template('sign_up.html')