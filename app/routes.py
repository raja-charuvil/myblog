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
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.created_at.desc()).paginate(
        page, flask_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=blogs.next_num) \
        if blogs.has_next else None
    prev_url = url_for('index', page=blogs.prev_num) \
        if blogs.has_prev else None
    return render_template(
        'index.html',
        title='Home',
        blogs=blogs.items,
        next_url=next_url,
        prev_url=prev_url)


@flask_app.route('/about_raja')
def about_raja():
    return render_template('about_raja.html', title='About Raja')


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
def all_blogs():
    blogs = Blog.query.all()
    return render_template('blogs.html', title='All Blogs', blogs=blogs)


@flask_app.route('/blog/<int:id>', methods=["GET"])
def get_single_blog(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    return render_template('get_single_blog.html', title=blog.title, blog=blog) 


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
