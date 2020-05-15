from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from db.db import db
from forms.login_forms import LoginForm, SignupForm
from models.login_models import User
from datetime import datetime

login_app = Blueprint('login_auth', __name__)


@login_app.route('/', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()  # Validate Login Attempt
            if user and user.check_password(password=password):
                user.authenticated = True
                user.last_login = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                session['user_logged_email'] = user.email
                return redirect('dashboard')
        flash('Invalid username/password combination', 'error')
        return redirect('/')
    return render_template('index.html', form=login_form)


@login_app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    email = session['user_logged_email']
    user = User.query.filter_by(email=email).one()  # Check if user exists
    user.authenticated = False
    db.session.commit()
    if session.get('user_logged_in'):
        # prevent flashing automatically logged out message
        del session['user_logged_in']
    flash('You have successfully logged yourself out.', 'success')
    return redirect('/')


@login_app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST':
        print(signup_form)
        if signup_form.validate_on_submit():
            email = signup_form.email.data
            password = signup_form.password.data
            print(email)
            existing_user = User.query.filter_by(email=email).first()  # Check if user exists
            if existing_user is None:
                user = User(email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()  # Create new user
                flash('Your account created Successfully.!!')
                return redirect('/')
            flash('A user already exists with that email address.')
            return redirect('signup')
        flash('User form not valid')
    return render_template('register.html', form=signup_form)


@login_app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('admin_web/dashboard.html', current_user=current_user)
