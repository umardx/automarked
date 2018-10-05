from flask              import render_template, redirect, url_for, request, flash
from flask_login        import login_required, login_user, current_user, logout_user
from automarked         import app, db, login_manager, app_name
from werkzeug.security  import generate_password_hash, check_password_hash
from automarked.models  import LoginForm, SignupForm, ForgotEmailForm, Users, \
                        ChangePasswordForm, AddDeviceForm


# Set log in view
login_manager.login_view = 'login'

# Load user from User models
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    title = 'Login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.isActive and check_password_hash(user.password, form.password.data):
            flash(u'You were successfully logged in, as ' + user.username, 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash(u'Invalid credentials.', 'error')
    return render_template('login.html', form=form, title=title, app_name=app_name)

@app.route('/forgot_password')
def forgot_password():
    title = 'Forgot Password'
    form = ForgotEmailForm()
    return render_template('forgot.html', form=form, title=title, app_name=app_name)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You have been successfully logged out.', 'success')
    return redirect(url_for('index'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    _err = None
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    title = 'Signup'
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_user = Users(
            isActive = form.accept_tos.data,
            username = form.username.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash(u'You account has been created.', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html',form=form, title=title, _err=_err, app_name=app_name)

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    title = 'Dashboard'
    userProfileForm = ChangePasswordForm()
    return render_template('dashboard.html', title=title, app_name=app_name, userProfileForm=userProfileForm)

@app.route('/dashboard/change_password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = generate_password_hash(form.password.data, method='sha256')
            db.session.add(user)
            db.session.commit()
            flash(u'You have been successfully changes your password.', 'success')
        else:
            for field in form.errors:
                for err in form.errors[field]:
                    flash(u'Can\'t change your password. ' + err, 'error')
                    break
    return redirect(url_for('dashboard'))

@app.route('/dashboard/add_device', methods = ['GET', 'POST'])
@login_required
def add_device():
    title = 'Add Device'
    userProfileForm = ChangePasswordForm()
    addDeviceForm = AddDeviceForm()
    if request.method == 'POST':
        if AddDeviceForm.validate_on_submit():
            pass

    return render_template('add_device.html', title=title, app_name=app_name, userProfileForm=userProfileForm, addDeviceForm=addDeviceForm)

@app.route('/dashboard/list_device')
@login_required
def list_device():
    title = 'List Device'
    userProfileForm = ChangePasswordForm()
    return render_template('list_device.html', title=title, app_name=app_name, userProfileForm=userProfileForm)

@app.route('/dashboard/yang_explorer')
@login_required
def yang_explorer():
    title = 'YANG Explorer'
    userProfileForm = ChangePasswordForm()
    return render_template('yangExplr.html', title=title, app_name=app_name, userProfileForm=userProfileForm)

# TODO
# [x] register unique username or email
# [x] flask session
# [ ] flask security 
# [ ] create dashboard layout
# [ ] ncclient https://ncclient.readthedocs.io/en/latest/
# Ref: https://www.youtube.com/watch?v=8aTnmsDMldY&t=1397s
