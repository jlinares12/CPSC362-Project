from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#pip install flask_bcrypt
from flask_bcrypt import Bcrypt
#pip install flask_login
from flask_login import LoginManager

app = Flask(__name__)   # Create an instance of a FLASK app called app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db' # Tells python where the sqlite database is stored
app.config['SECRET_KEY'] = 'd4d850ac4be6b386b7b3c5ab' # Saves a secret key to be able to prevent CSRF
db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter
bcrypt = Bcrypt(app)    # Create an instance of Bcrypt using our app as a parameter
login_manager = LoginManager(app)

from community_garden import routes