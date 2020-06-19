from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField, PasswordField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, url
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', [DataRequired(), EqualTo('password')])
    description = StringField('Your Description', [DataRequired()])
    experience = StringField('Your Experience', [DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    job_content = TextAreaField('Job Description', validators=[DataRequired()])
    job_experience = TextAreaField('Experience Required', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    type = SelectField('Job Type', choices=[('Internship', 'Internship'), ('Full Time', 'Full Time'), ('Part Time', 'Part Time')])
    tag = StringField('Job tags')
    website = StringField('Company Website', validators=[url()])
    close = DateField('Closing Date', format='%m/%d/%Y')
    submit = SubmitField('Post')


class ApplyForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('First and Last Name', validators=[DataRequired()])
    apply = TextAreaField('Why you should get the job', validators=[DataRequired()])
    submit = SubmitField('Apply')

class SearchForm(FlaskForm):
    search = StringField('What job are you looking for today?', validators=[DataRequired()])
    submit = SubmitField('Search')


