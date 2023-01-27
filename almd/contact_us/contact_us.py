from flask import Blueprint, render_template
from models.models import ContactForm
import os
# from controler.controler import db
from models.models import Article

contact_bp = Blueprint(
    'contact_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
    )  # create blueprint inorder to render the news package


@contact_bp.route('/')
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        pass #TODO: impliment information for sending form data here
    return render_template('contact-us/contact-us.html', form=form)
