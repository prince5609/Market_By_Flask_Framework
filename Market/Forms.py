from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Market.Models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username Already Exist, Try Another One")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email Address Already Exist, Try Another one")

    username = StringField(label=" Enter Your Name", validators=[Length(min=5, max=15), DataRequired()])
    email_address = StringField(label="Enter Email_Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Enter Password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm your Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    email_address = StringField(label="Email Address:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase")


class ReturnItemForm(FlaskForm):
    submit = SubmitField(label="Return")
