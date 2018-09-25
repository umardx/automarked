from os import environ
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, current_user, logout_user
from automarked import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from automarked.models import err_msg, LoginForm, SignupForm, User


def getAppName():
    app_name = str(environ.get('APP_NAME'))
    return app_name

# Set log in view
login_manager.login_view = 'login'

# Load user from User models
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    app_name = getAppName()
    title = 'Login — ' + app_name
    sign_err = None
    sign_msg = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                sign_msg = 'You were successfully logged in'
                login_user(user, remember=form.remember.data)
            else:
                sign_err = 'Get the fuck out here!'
    return render_template('login.html', form=form, title=title, app_name=app_name, sign_msg=sign_msg, sign_err=sign_err)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    app_name = getAppName()
    title = 'Signup — ' + app_name
    sign_err = None
    sign_msg = None
    form = SignupForm()

    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if username:
            sign_err = 'You\'re idiot! The username is already registered.'
        elif email:
            sign_err = 'You\'re idiot! The email is already registered.'
        else:
            new_user = User(
                isActive = True,
                username = form.username.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            sign_msg = 'Account has been created!'

    return render_template('signup.html',form=form, title=title, app_name=app_name, sign_msg=sign_msg, sign_err=sign_err)

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    app_name = getAppName()
    title = 'Dashboard — ' + app_name
    return render_template('dashboard.html', title=title, app_name=app_name)

# TODO
# [ ] register unique username or email
# [x] flask session
# [ ] flask security 
# Ref: https://www.youtube.com/watch?v=8aTnmsDMldY&t=1397s