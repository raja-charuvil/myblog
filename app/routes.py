from flask import request, jsonify, render_template
from app import flask_app
from app.models import Blog, Tag


@flask_app.route('/')
@flask_app.route('/index')
def index():
	blogs = [
        {
            'title': 'Python for beginners',
            'content': 'Python is very simple language'
        },
        {
            'title': 'Scala',
            'content': 'Scala is very smart language'
        }
    ]
	return render_template('index.html', title='Home', blogs=blogs)


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

@flask_app.route('/update_blog/<int:id>', methods=["PUT"])
def update_blog(id):
	data = request.get_json()
	blog = Blog.query.filter_by(id=id).first_or_404()

	blog.title = data["title"]
	blog.content = data["content"]
	blog.feature_image = data["feature_image"]

	updated_blog = blog.serialize

	db.session.add()
	return jsonify({"blog_id": blog.id})

@flask_app.route('/delete_blog/<int:id>', methods=["DELETE"])
def delete_blog(id):
	blog = Blog.query.filter_by(id=id).first()
	db.session.delete(blog)
	db.session.commit()

	return jsonify({"Blog was deleted!"}), 200
