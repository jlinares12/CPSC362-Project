# run in terminal on laptop: pip install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from community_garden.models import User

class RegisterForm( FlaskForm ):
    def validate_username(self, username_to_validate):
        user = User.query.filter_by(username=username_to_validate.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email(self, email_to_validate):
        email = User.query.filter_by( email=email_to_validate.data ).first()
        if email:
            raise ValidationError('Email address already exists!')

    name = StringField( label='name', validators=[Length(min=3, max=50), DataRequired()] )
    username = StringField( label='username', validators=[Length(max=65), DataRequired()])
    email = StringField( label='email', validators=[Length(min=3, max=65), Email(), DataRequired()])
    password1 = PasswordField( label='password1', validators=[Length(min=10), DataRequired()] )
    password2 = PasswordField( label='password2', validators=[EqualTo('password1'), DataRequired()] )
    submit = SubmitField( label='Sign up' )

class LoginForm (FlaskForm ):
    username = StringField( label="Username", validators=[Length(min=3, max=50), DataRequired()])
    password = PasswordField( label='Password', validators=[Length(min=10), DataRequired()] )
    submit = SubmitField( label='Login' )