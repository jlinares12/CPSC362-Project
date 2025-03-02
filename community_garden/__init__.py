#pip install flask-sqlalchemy next time you run native on laptop
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # Create an instance of a FLASK app called app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db' # Tells python where the sqlite database is stored

app.config['SECRET_KEY'] = 'd4d850ac4be6b386b7b3c5ab' # Saves a secret key to be able to prevent CSRF

db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter

from community_garden import routes