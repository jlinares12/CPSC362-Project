# run in terminal on laptop: pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm( FlaskForm ):
    name = StringField( label='name' )
    username = StringField( label='username' )
    email_address = StringField( label='email' )
    password1 = PasswordField( label='password1' )
    password2 = PasswordField( label='password2' )
    submit = SubmitField( label='Sign up' )