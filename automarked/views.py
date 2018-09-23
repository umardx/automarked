from flask import render_template, redirect, url_for
from automarked import app, db
from automarked.models import LoginForm, SignupForm, User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            return redirect(url_for('dashboard'))
        return "<h1>Invalid Username or Password!</h1>"

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Account has been created!</h1>'

    return render_template('signup.html',form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')