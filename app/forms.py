from flask_wtf import FlaskForm
from wtforms import validators, SubmitField, StringField, PasswordField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
from app.hypervisor import get_hypervisor_nodes
from app.models import User

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class AddVMForm(FlaskForm):
    node = SelectField('Hypervisor Node', choices=get_hypervisor_nodes())
    vm_id = SelectField('Virtual Machine', choices=[])
    submit = SubmitField('Add VM')

