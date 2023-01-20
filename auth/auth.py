from flask import render_template, redirect, url_for, request, current_app
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models.models import Admin, RegisterForm, LoginForm
from factory.factory import db
import os



# Todo: Add admin only to form to prevent unintentional post
# https://gist.github.com/angelabauer/36083610dcdcbe704b3c30b51e2fe414


auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)  # create blueprint inorder to render the news package


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()

        if username and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('auth_bp.private'))

    return render_template("login/login.html", form=form)


@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_admin = Admin(
            username=form.username.data,
            password=hash_and_salted_password
        )
        db.session.add(new_admin)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('register/register.html', form=form)


@auth_bp.route('private', methods=["POST", "GET"])
@login_required
def private():
    return render_template('private/private.html')


@auth_bp.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('home'))

# https://flask-login.readthedocs.io/en/latest/
# https://gist.github.com/angelabauer/f53574e00338a08e989c3c983506a8ba
