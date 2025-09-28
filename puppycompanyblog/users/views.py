# users/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm,UpdateForm
from puppycompanyblog.users.picture_handler import add_profile_pic
users = Blueprint('users', __name__)

# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check for existing username
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        # Check for existing email (optional)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different one.', 'danger')
            return render_template('register.html', form=form)

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        from sqlalchemy.exc import IntegrityError

        db.session.add(user)
        try:
            db.session.commit()
            flash('Thanks for registering!', 'success')
            return redirect(url_for('users.login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)


# @users.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email = form.email.data,
#                     username = form.username.data,
#                     password = form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash("Thanks for registration!")
#         return redirect(url_for('users.login'))
#     return render_template("register.html", form=form)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login success!")

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('core.index')
            return redirect(next_page)

        flash("Invalid email or password.")  # Optional: feedback on failure

    return render_template("login.html", form=form)  # Always return this


# logout

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))

# account (Update Userform)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
            if form.picture.data:
                username= current_user.username
                pic = add_profile_pic(form.picture.data, username)
                current_user.profile_image = pic

            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account has been updated!")
            return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


# User's list of blog posts.
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(user_id=user.id).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)




