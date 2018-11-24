from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, Email, EqualTo
from app.models import User
from flask_wtf.file import FileField,FileRequired,FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    useremail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, useremail):
        user = User.query.filter_by(useremail=useremail.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InfoForm(FlaskForm):
    infotitle=StringField('Title',validators=[DataRequired()])
    infocontent=StringField('Content',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AProblem(FlaskForm):
    problemtitle=StringField('Problem',validators=[DataRequired()])
    problemdescription=StringField('Description',validators=[DataRequired()])
    probleminput=StringField('Input',validators=[DataRequired()])
    problemoutput=StringField('Output',validators=[DataRequired()])
    problemsampleinput=StringField('Sample Input',validators=[DataRequired()])
    problemsampleoutput=StringField('Sample Output',validators=[DataRequired()])
    problemhint=StringField('Hint',validators=[DataRequired()])
    problemsource=StringField('Source',validators=[DataRequired()])
    problemtest=FileField('Test Data',validators=[FileRequired()])
    problemans=FileField('Test Answer',validators=[FileRequired()])
    problemms=StringField('MS',validators=[DataRequired()])
    problemkb=StringField('KB',validators=[DataRequired()])
    submit = SubmitField('Submit')

class SProblem(FlaskForm):
    submit=SubmitField('Submit')

class Submission(FlaskForm):
    problemid=StringField('Problem Id',validators=[DataRequired()])
    status=SelectField('Language',validators=[DataRequired()],choices=[('0','C++'),('1','Java'),('2','Python')])
    code=StringField('Code',validators=[DataRequired()])
    submit=SubmitField('Submit')
