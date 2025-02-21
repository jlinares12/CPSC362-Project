from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/register')
def register_page():
    return render_template('register_page.html')