#pip install flask-sqlalchemy next time you run native on laptop
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # Create an instance of a FLASK app called app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter

user_garden_volunteer = db.Table(
    'user_garden_volunteer',  # Name of the table
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),  # Foreign key to User
    db.Column('garden_id', db.Integer(), db.ForeignKey('garden.id'), primary_key=True)  # Foreign key to Garden
)

class User(db.Model):
    id = db.Column( db.Integer(), primary_key=True, nullable=False, unique=True )
    name = db.Column( db.String(length=30), nullable=False, unique=True )
    email = db.Column( db.String(length=320), nullable=False, unique=True)
    # Relationship to Garden (assuming a Garden table exists)
    administered_gardens = db.relationship('Garden', backref='admin', lazy=True)

    volunteer_gardens = db.relationship(
        'Garden',  # Target model
        secondary=user_garden_volunteer,  # Association table
        backref='volunteers'  # Name of the reverse relationship
    )

    def __repr__(self):
        return f'{self.name}'

class Garden(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(length=50), nullable=False)
    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    
    def __repr__(self):
        return f'{self.name}'

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