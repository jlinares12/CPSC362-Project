# run in terminal on laptop: pip install flask-wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, URLField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from community_garden.models import User, Garden

class RegisterUserForm( FlaskForm ):
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
    username = StringField( label="Username", validators=[DataRequired()])
    password = PasswordField( label='Password', validators=[DataRequired()] )
    submit = SubmitField( label='Login' )

class RegisterGardenForm( FlaskForm ):
    name = StringField( label="name", validators=[DataRequired()])
    street_address = StringField( label="street", validators=[DataRequired()])
    city = StringField( label="city", validators=[DataRequired()])
    state = StringField( label="state", validators=[DataRequired()])
    zip_code = StringField( label="zip code", validators=[DataRequired()])
    hours_of_operation = StringField( label="Hours of operation", validators=[DataRequired()])
    description = TextAreaField( label="description", validators=[DataRequired()])
    wish_list = TextAreaField( label="wish list", validators=[DataRequired()])
    donation_link = URLField( label="donation link", validators=[DataRequired()])
    photo = FileField('photo',validators=[FileRequired()])
    submit = SubmitField( label='Register' )

    def validate_street_address(self, address_to_validate):
        garden = Garden.query.filter_by(street_address=address_to_validate.data).first()
        if garden:
            raise ValidationError('A garden with that address already exists!')
    def validate_description(self, description_to_validate):
        garden = Garden.query.filter_by(description=description_to_validate.data).first()
        if garden:
            raise ValidationError('A garden with that description already exists!')