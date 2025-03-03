# run in terminal on laptop: pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm( FlaskForm ):
    name = StringField( label='name', validators=[Length(min=3, max=50), DataRequired()] )
    username = StringField( label='username', validators=[Length(max=65), DataRequired()])
    email = StringField( label='email', validators=[Length(min=3, max=65), Email(), DataRequired()])
    password1 = PasswordField( label='password1', validators=[Length(min=10), DataRequired()] )
    password2 = PasswordField( label='password2', validators=[EqualTo('password1'), DataRequired()] )
    submit = SubmitField( label='Sign up' )