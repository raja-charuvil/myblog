from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField,\
	SubmitField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()]) 
	content = TextAreaField('content', validators=[DataRequired()])
	feature_image = StringField('image')
	created_at = DateTimeField('created at')
	tags = StringField('tags')
	submit = SubmitField('Create')
