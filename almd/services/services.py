from flask import Blueprint, render_template
import os


services_bp = Blueprint(
    'services_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)  # create blueprint inorder to render the services package


@services_bp.route('/services')
def services():
    return render_template('services/services_page.html')
