from os import environ
from flask import render_template, redirect, url_for, request, flash
from automarked import app, db, hs
from automarked.models import LoginForm, SignupForm, User

def getAppName():
    try:
        app_name = str(environ.get('APP_NAME'))
    except:
        app_name = 'Automarked'
    return app_name

@app.route('/', methods=['GET', 'POST'])
def index():
    app_name = getAppName()
    title = 'Home — ' + app_name
    sign_err = None
    sign_msg = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and hs.check_password_hash(user.password, form.password.data):
                sign_msg = 'You were successfully logged in'
            else:
                sign_err = 'Get the fuck out here!'
    return render_template('index.html', form=form, title=title, app_name=app_name, sign_msg=sign_msg, sign_err=sign_err)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    app_name = getAppName()
    title = 'Signup — ' + app_name
    sign_err = None
    sign_msg = None
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = hs.generate_password_hash(form.password.data).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        sign_msg = 'Account has been created!'

    return render_template('signup.html',form=form, title=title, app_name=app_name, sign_msg=sign_msg, sign_err=sign_err)

@app.route('/dashboard')
def dashboard():
    app_name = getAppName()
    title = 'Dashboard — ' + app_name
    return render_template('dashboard.html', title=title, app_name=app_name)

# TODO
# [] register unique username or email
# [] flask session
# [] flask security 