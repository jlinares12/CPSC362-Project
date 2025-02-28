#pip install flask-sqlalchemy next time you run native on laptop
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # Create an instance of a FLASK app called app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter

from community_garden import routes