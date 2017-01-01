from flask_wtf import FlaskForm as Form
from wtforms import (StringField, PasswordField, TextAreaField,
                     DateTimeField, SelectField)
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from model import User
##custom validator
## raises error if username already exists
##notice you dont pass this to validators as
## name_exists() but as name_exists
##no ()
def name_exists(form, field):
    """custom name-exists validator"""
    ##.exists() is a peewee method
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists.")
def email_exists(form, field):
    """custom email-exists validator"""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists.")

##Register Form object
class RegisterForm(Form):
    """register form object"""
    ##Every variable here is a field definiton
    ##For fields you create appropriate field type
    ## and fill it in with label and validators list.
    username = StringField(
        ##label
        "Username",
        ##conventionally
        ##defining them to validators looks better i guess
        validators=[
            DataRequired(),
            ##i suppose we could just use \w on regex
            ##This validator takes two argument
            ##first one is regx obj,secon one is its message
            Regexp(r"^[a-zA-Z0-9_]+$",
                   message="Username should be one word, letters,numbers, and underscores only"),
            name_exists ##we define this validator ourselves
        ]
    )

    firstname = StringField(
        "First name",
        validators=[
            DataRequired()
        ]
    )

    lastname = StringField(
        "Last name",
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            email_exists,##we define this validator ourselves
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo("password2", message="Passwords must match")
        ]
    )

    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired()]
    )

##we'll validate this in view.
class LoginForm(Form):
    """Login form object"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

class PostForm(Form):
    """Post form object"""
    content = TextAreaField("Type stuff", validators=[DataRequired()])

class EventForm(Form):
    """Event form object"""
    eventname = StringField("Event name", validators=[DataRequired()])
    eventdatetime = DateTimeField("Y-m-d H:M:S", format="%Y-%m-%d %H:%M:%S")
    eventcontent = TextAreaField("Type what you type to announcement mails.")
    eventtype = SelectField("", choices=[("0", "ori-ing"), ("1", "runnning")])
    eventday = SelectField("Event Day", choices=[("2", "wednesday"),
                                                 ("5", "saturday"),
                                                 ("6", "sunday")])
