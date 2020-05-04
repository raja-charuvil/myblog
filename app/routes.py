import mistune
from flask import request, jsonify, render_template, redirect, \
	url_for
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user
from app import flask_app, db
from app.models import Blog, Tag, User
from app.forms import BlogForm, LoginForm


@flask_app.route('/')
@flask_app.route('/index')
def index():
	blogs = Blog.query.all()
	return render_template('index.html', title='Home', blogs=blogs)


@flask_app.route('/add_blog', methods=["GET", "POST"])
@login_required
def add_blog():
	form = BlogForm()
	if form.validate_on_submit():
		new_blog = Blog(
			title=form.title.data,
			content=mistune.html(form.content.data))

		if form.tags.data:
			blog_tags = [x.strip() for x in form.tags.data.split(",")]
			for tag in blog_tags:
				present_tag = Tag.query.filter_by(name=tag).first()
				if (present_tag):
					present_tag.blogs_associated.append(new_blog)
				else:
					new_tag = Tag(name=tag)
					new_tag.blogs_associated.append(new_blog)
					db.session.add(new_tag)

		db.session.add(new_blog)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template('add_blog.html', title='add blog', form=form)

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

@flask_app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=False)
				return redirect(url_for('add_blog'))
	return render_template('admin_login.html', title='Sign In', form=form)
