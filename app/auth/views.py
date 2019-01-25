from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from app.auth import auth
from app.auth.forms import SignInForm, SignupForm, ForgotForm
from app import db
from app.models import Users

# Logout route
@auth.route('/signout')
@login_required
def signout():
    """
    Handle requests to the /signout route
    """
    logout_user()
    flash(u'You have been successfully logged out.', 'success')
    return redirect(url_for('auth.signin'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle requests to the /signup route
    Add an user to the database through the registration form
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    formSignUp = SignupForm()

    if request.method == 'POST' and formSignUp.validate_on_submit():
        _user = Users(
            isActive=formSignUp.accept_tos.data,
            username=formSignUp.username.data,
            email=formSignUp.email.data,
            password=formSignUp.password.data
        )

        try:
            db.session.add(_user)
            db.session.commit()
            flash(u'You account has been created.', 'success')
        except Exception as e:
            flash(u'Can\'t add account to the database.' + str(e), 'error')

        return redirect(url_for('auth.signin'))

    return render_template('auth/signup.html', title='Sign Up | Auth', form=formSignUp)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Handle requests to the /signin route
    Log an user in through the signin form
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    formSignIn = SignInForm()

    if request.method == 'POST' and formSignIn.validate_on_submit():
        _user = Users.query.filter_by(username=formSignIn.username.data).first()
        if _user and _user.isActive and _user.check_password(formSignIn.password.data):
            login_user(_user, remember=formSignIn.remember.data)
            flash(u'You were successfully logged in, as ' + _user.username, 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash(u'Invalid credentials.', 'error')
    
    return render_template('auth/signin.html', title='Sign In | Auth', form=formSignIn)


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot():
    """
    Handle requests to the /forgot_password route
    Reset password account
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    formForgot = ForgotForm()

    if request.method == 'POST' and formForgot.validate_on_submit():
        _user = Users.query.filter_by(email=formForgot.email.data).first()
        if _user:
            flash(u'Email sent to ' + _user.email + ' with username ' + _user.username, 'success')
        else:
            flash(u'Email address not found.', 'error')
    
    return render_template('auth/forgot.html', title='Forgot Password | Auth', form=formForgot)


@auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """
    Handle requests to the /change_password route
    """
    return redirect(url_for('dashboard.index'))


