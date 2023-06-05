from flask import Blueprint, render_template
import os

#from controler.controler import db
from models.models import Article


resources_bp = Blueprint(
    'resources_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)


@resources_bp.route('/gis-portal')
def resources():
    return render_template('resources/gis_portal.html')