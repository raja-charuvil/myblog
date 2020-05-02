from flask import request, jsonify
from app import flask_app
from app.models import Blog, Tag


@flask_app.route('/')
@flask_app.route('/index')
def index():
	return "Hello world!"


@flask_app.route('/add_blog', methods=["POST"])
def create_blog():
	data = request.get_json()

	new_blog = Blog(
		title=data["title"],
		content=data["content"],
		feature_image=data["feature_image"])

	for tag in data["tags"]:
		present_tag = Tag.query.filter_by(name=tag).first()
		if (present_tag):
			present_tag.blogs_associated.append(new_blog)
		else:
			new_tag = Tag(name=tag)
			new_tag.blogs_associated.append(new_blog)
			db.session.add(new_tag)

	db.session.add(new_blog)
	db.session.commit()

	blog_id = getattr(new_blog)
	return jsonify({"id": blog_id})
