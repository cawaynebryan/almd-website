from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, FileField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired
from flask_ckeditor.fields import CKEditorField
from flask import current_app


class CatalogueForm(FlaskForm):
    title = StringField('Article Title', validators=[InputRequired()])
    date = DateField('Date Posted', validators=None, format="%Y-%m-%d")
    image = FileField('Image')
    article = CKEditorField('Article', validators=[InputRequired()])
    submit = SubmitField('Submit Article')


class RegisterForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[InputRequired()])
    email = StringField(label='Email', validators=[InputRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message', render_kw={"rows": 10, "cols": 70}, validators=[InputRequired()])