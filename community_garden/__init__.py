from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_uploads import  configure_uploads, IMAGES, UploadSet
from geopy.geocoders import Nominatim
from flask_migrate import Migrate
from flask_mail import Mail
import os

load_dotenv()
app = Flask(__name__)   # Create an instance of a FLASK app called app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') # Tells python where the sqlite database is stored
app.config['SECRET_KEY'] = os.getenv('DEV_KEY') # Saves a secret key to be able to prevent CSRF
app.config['UPLOADED_PHOTOS_DEST'] = 'community_garden/static/img'
photos = UploadSet('photos', IMAGES)
jawg_token = os.getenv('JAWG_API_KEY')
configure_uploads(app, photos)
db = SQLAlchemy(app)    # Create an instance of SQLAlchemy called db that takes our flask app as a parameter
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)    # Create an instance of Bcrypt using our app as a parameter
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'danger'

# Config for mailing feature

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

geolocator = Nominatim(user_agent="community_garden_flask_app")
from community_garden import routes