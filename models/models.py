from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

from factory.factory import db
from flask_login import UserMixin


def formatted_time():
    return datetime.utcnow().strftime("%Y-%m-%d")


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=formatted_time)
    title = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(5000), nullable=False)


class RegisterForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message', render_kw={"rows": 10, "cols": 40}, validators=[DataRequired()])

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return "Article database"
