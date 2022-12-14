from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, FileField
from wtforms.validators import InputRequired, URL, Email
from flask_ckeditor import CKEditorField


class CatalogueForm(FlaskForm):
    title = StringField('Article Title', validators=[InputRequired()])
    date = DateField('Date Posted', validators=None, format="%Y-%m-%d")
    image = FileField('Image')
    article = CKEditorField('Article', validators=[InputRequired()])
    submit = SubmitField('Submit Article')


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[InputRequired()])
    email = StringField('Your Email', validators=[InputRequired(), Email()])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')
