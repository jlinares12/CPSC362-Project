from community_garden import app
from flask import render_template, redirect, url_for, flash
from community_garden.models import User
from community_garden.forms import RegisterForm
from community_garden import db

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

@app.route('/login')
def login_page():
    return render_template('login_page.html')

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register_page.html', form=form)