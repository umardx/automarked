import os
from flask import render_template, redirect, url_for, request
from automarked import app, db, hs
from automarked.models import LoginForm, SignupForm, User

def getAppName():
    try:
        app_name = str(os.environ.get('APP_NAME'))
    except:
        app_name = 'Automarked'
    return app_name

@app.route('/', methods=['GET', 'POST'])
def index():
    app_name = getAppName()
    title = 'Home — ' + app_name
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and hs.check_password_hash(user.password, form.password.data):
                return redirect(url_for('dashboard'))
            return "<h1>Invalid Username or Password!</h1>"
    return render_template('index.html', form=form, title=title, app_name=app_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    app_name = getAppName()
    title = 'Signup — ' + app_name
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = hs.generate_password_hash(form.password.data).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Account has been created!</h1>'

    return render_template('signup.html',form=form, title=title, app_name=app_name)

@app.route('/dashboard')
def dashboard():
    app_name = getAppName()
    title = 'Dashboard — ' + app_name
    return render_template('dashboard.html', title=title, app_name=app_name)
