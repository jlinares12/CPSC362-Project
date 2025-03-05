from community_garden import app, db
from flask import render_template, redirect, url_for, flash
from community_garden.models import User
from community_garden.forms import RegisterUserForm, LoginForm
from flask_login import login_user, logout_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/resources')
def resources_page():
    return render_template('resources_page.html')

@app.route('/volunteer')
def volunteer_page():
    return render_template('volunteer_page.html')

@app.route('/donate')
def donations_page():
    return render_template('donations_page.html')

@app.route('/about')
def about_page():
    return render_template('about_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if not attempted_user:
            flash(f'That username was not found: ', category='danger')
        elif attempted_user.check_password_correction(
            form.password.data
            ):
            login_user(attempted_user)
            flash(f'Login was successful! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'The username and password did not match', category='danger')
    return render_template('login_page.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out!', category='success')
    return redirect(url_for('home_page'))

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'You created your account successfully! Welcome to the site', category='success')
        return redirect(url_for('login_page'))
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register_page.html', form=form)