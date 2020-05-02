from app import db
from datetime import datetime


tag_blog = db.Table(
	'tag_blog',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
	db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True))


class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), nullable=False)
	content = db.Column(db.Text, nullable=False)
	feature_image = db.Column(db.String)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	tags = db.relationship(
		'Tag',
		secondary=tag_blog,
		backref=db.backref('blogs_associated', lazy='dynamic'))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'title': self.title,
			'content': self.content,
			'feature_image': self.feature_image,
			'created_at': self.created_at,
		}

	def __repr__(self):
		return '<Blog {}>'.format(self.title)


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name
		}

	def __repr__(self):
		return '<Tag {}>'.format(self.name)
	

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), nullable=False)
	password = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return '<User {}>'.format(self.email)
