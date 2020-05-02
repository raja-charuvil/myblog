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

@flask_app.route('/blogs', methods=["GET"])
def get_all_blogs():
	blogs = Blog.query.all()
	serialized_data = []
	for blog in blogs:
		serialized_data.append(blog.serialize)

	return jsonify({"all_blogs": serialized_data})

@flask_app.route('/blog/<int:id>', methods=["GET"])
def get_single_blog(id):
	blog = Blog.query.filter_by(id=id).first()
	serialized_blog = blog.serialize
	serialized_blog["tags"] = []

	for tag in blog.tags:
		serialized_blog["tags"].append(tag.serialize)

	return jsonify({"single_blog": serialized_blog})
