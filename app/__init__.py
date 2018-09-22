from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from app.models import LoginForm, SignupForm

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'uSjGEQm2ZRUMM978uBtdLHNmdF9tLqFZSUutqy6b'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        return '<h1>' + form.email.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html',form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
