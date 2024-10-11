from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TicketForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    price = FloatField('Price', validators=[DataRequired()])
    available = BooleanField('Available')
    submit = SubmitField('Add Ticket')