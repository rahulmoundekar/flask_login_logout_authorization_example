from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('User Name', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])


class SignupForm(FlaskForm):
    """User Signup Form."""
    email = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'), DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
