from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import dotenv_values

secrets = dotenv_values(".env")
app = Flask(__name__)   # Create an instance of a FLASK app called app
app.config['SQLALCHEMY_DATABASE_URI'] = secrets['DATABASE_URI'] # Tells python where the sqlite database is stored
app.config['SECRET_KEY'] = secrets['DEV_KEY'] # Saves a secret key to be able to prevent CSRF
db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter
bcrypt = Bcrypt(app)    # Create an instance of Bcrypt using our app as a parameter
login_manager = LoginManager(app)

from community_garden import routes