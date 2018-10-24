# app/home/views.py

from flask import render_template, \
    redirect, url_for
from flask_login import login_required

from app.home import home
from app.tasks import reverse, reverse_ten


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Home")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return redirect(url_for('dashboard.index'))


@home.route('/reverse/<string>')
def rev(string):
    res = reverse.delay(string)
    return str(res)


@home.route('/reverseten/<string>')
def revten(string):
    res = reverse_ten.delay(string)
    return str(res)
