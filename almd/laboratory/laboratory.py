from flask import Blueprint, render_template
import os


lab_bp = Blueprint(
    'lab_bp', __name__, template_folder='template',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)




@lab_bp.route('/')
def lab_page():
    return render_template('laboratory_page.html')
