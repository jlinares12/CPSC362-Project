from community_garden import app, db, photos, jawg_token
from flask import render_template, redirect, url_for, flash, request
from community_garden.models import User, Garden, user_garden_volunteer
from community_garden.forms import RegisterUserForm, LoginForm, RegisterGardenForm, VolunteerSignUpForm, UpdateGardenForm, UpdateUserForm, ValidationError
from flask_login import login_user, logout_user, login_required, current_user
from django.utils.http import url_has_allowed_host_and_scheme
import folium

def create_map():
    token = jawg_token
    tiles = (f"https://tile.jawg.io/jawg-sunny/{{z}}/{{x}}/{{y}}{{r}}.png?access-token={token}")
    attr = ('<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    map = folium.Map(location=[33.870350,-117.924301],tiles=tiles, attr=attr, zoom_start=10)
    return map

@app.route("/")
@app.route("/home")
def home_page():
    garden_map = create_map()
    gardens = Garden.query.all()
    for garden in gardens:
        folium.Marker([garden.latitude, garden.longitude]).add_to(garden_map)
    return render_template('home.html', gardens=gardens, map=garden_map._repr_html_())

@app.route('/search')
def search():
    garden_map = create_map()
    q = request.args.get('q')
    if q:
        gardens = Garden.query.filter(Garden.street_address.icontains(q) | Garden.city.icontains(q) | Garden.name.icontains(q) ).limit(20).all()
    else:
        gardens = Garden.query.all()
    for garden in gardens:
            folium.Marker([garden.latitude, garden.longitude]).add_to(garden_map)
    return render_template('partials/search_results.html', gardens=gardens, map=garden_map._repr_html_(), q=q)

@app.route('/resources')
def resources_page():
    return render_template('resources_page.html')

@app.route('/about-us')
def about_us_page():
    return render_template('about_us_page.html')

@app.route('/garden-profile/<garden>')
def garden_profile(garden):
    current_garden = Garden.query.filter_by(name=garden).first()
    return render_template('garden_profile.html', garden = current_garden)

@app.route('/profile/<username>')
@login_required
def profile_page(username):
    # Ensure the username in the URL matches the logged-in user
    if username != current_user.username:
        return redirect(url_for('profile_page', username=current_user.username))
    return render_template('profile_page.html', username=current_user.username)

@app.route('/profile')
@login_required
def redirect_to_profile():
    # Redirect to the profile page with the logged-in user's username
    return redirect(url_for('profile_page', username=current_user.username))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if not attempted_user or not attempted_user.check_password_correction(form.password.data):
            flash(f'Invalid username or password', category='danger')
            return redirect(url_for('login_page'))
        login_user(attempted_user)
        next = request.args.get('next')
        flash(f'Login was successful! You are logged in as: {attempted_user.username}', category='success')
        if not url_has_allowed_host_and_scheme(next, request.host):
            return redirect(url_for('home_page'))
        return redirect(next)
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
        login_user(user_to_create)
        flash(f'You created your account successfully! Welcome to the site {user_to_create.username}', category='success')
        return redirect(url_for('profile_page', username=current_user.username))
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg[0]}', category='danger')
    return render_template('register_page.html', form=form)

@app.route('/register-garden', methods=['GET', 'POST'])
@login_required
def register_garden():
    form = RegisterGardenForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        garden_to_create = Garden(
            name = form.name.data,
            street_address = form.street_address.data,
            city = form.city.data,
            state = form.state.data,
            zip_code = form.zip_code.data,
            hours_of_operation = form.hours_of_operation.data,
            description = form.description.data,
            wish_list = form.wish_list.data,
            donation_link = form.donation_link.data,
            admin_id = current_user.id,
            photo = filename, )
        garden_to_create.create_coordinates()
        db.session.add(garden_to_create)
        db.session.commit()
        flash(f'You created {garden_to_create.name} successfully!', category='success')
        return redirect(url_for('profile_page', username=current_user.username))
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating your garden: {err_msg[0]}', category='danger')
    return render_template('register_garden.html', form=form)

@app.route('/volunteer-sign-up/<garden>', methods=['GET', 'POST'])
@login_required
def volunteer_sign_up(garden):
    current_garden = Garden.query.filter_by(name=garden).first()
    form = VolunteerSignUpForm()
    if form.validate_on_submit():
        volunteer = user_garden_volunteer.insert().values(user_id=current_user.id, garden_id=current_garden.id)
        try:
            db.session.execute(volunteer)
            db.session.commit()
        except:
            db.session.rollback()
        flash(f'You signed up to volunteer at {current_garden.name} successfully!', category='success')
        return redirect(url_for('profile_page', username=current_user.username))
    return render_template('volunteer.html', form=form, garden=current_garden)

@app.route('/update-garden-info<garden>', methods=['GET', 'POST'])
@login_required
def update_garden(garden):
    curr_garden = Garden.query.filter_by(name=garden).first()
    form = UpdateGardenForm()
    if form.validate_on_submit():
        for field in form:
            if field.data:
                setattr(curr_garden, field.name, field.data)
        db.session.commit()
        flash(f'You have updated the info for {curr_garden.name} successfully!', category='success')
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating your garden: {err_msg[0]}', category='danger')
    return render_template('update_garden.html', form=form, garden=curr_garden )

@app.route('/update-user-info/<username>', methods=['GET', 'POST'])
@login_required
def update_user(username):
    form = UpdateUserForm()
    form.curr_email = current_user.email
    form.curr_username = current_user.username
    if form.validate_on_submit():
        if current_user.check_password_correction(form.password.data):
            flash(f'There as an error updating your info: Your new password cannot be the same as your old password', category='danger')
            return redirect(url_for('update_user', username = current_user.username))
        for field in form:
            if field.data:
                setattr(current_user, field.name, field.data)
        db.session.commit()
        flash(f'You have updated the info for {current_user.name} successfully!', category='success')
    if form.errors != {}:                                           # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error updating your info: {err_msg[0]}', category='danger')
    return render_template('update_user.html', form=form, user=current_user )