from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField,\
	SubmitField, PasswordField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()]) 
	content = TextAreaField('content', validators=[DataRequired()])
	feature_image = StringField('image')
	created_at = DateTimeField('created at')
	tags = StringField('tags')
	submit = SubmitField('Create')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')
