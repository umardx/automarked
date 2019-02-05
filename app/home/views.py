# app/home/views.py

from flask import render_template, redirect, url_for
from flask_login import login_required

from app.home import home
from app.tasks import reverse


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


@home.route('/robots.txt')
def robots_txt():
    Disallow = lambda string: 'Disallow: {0}'.format(string)
    return Response('User-agent: *\n{0}\n'.format('\n'.join([
        Disallow('/bin/*'),
        Disallow('/thank-you'),
    ])))


@home.route('/reverse/<string>')
def rev(string):
    res = reverse.delay(string)
    return str(res)
