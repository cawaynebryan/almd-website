from flask import Blueprint, render_template
import os
#from controler.controler import db
from models.models import Article

about_bp = Blueprint(
    'about_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
    )  # create blueprint inorder to render the news package


@about_bp.route('/')
def about_us():
    return render_template('about-us/about-us.html')