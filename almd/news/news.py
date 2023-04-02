from flask import current_app, flash
from flask import Blueprint, render_template, redirect, url_for
from factory.factory import db
from werkzeug.utils import secure_filename
from almd.forms.forms import CatalogueForm
from flask_login import login_required
from models.models import Article
import requests



from datetime import date
import requests
import os


news_bp = Blueprint(
    'news_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)


ADDRESS = 'http://127.0.0.1'
PORT = 5000
HOST_AND_PORT = f'{ADDRESS}:{PORT}'


# ################################################## NEWS  #############################################################

@news_bp.route('/')
def news_catalogue():
    articles = requests.get(HOST_AND_PORT + url_for('api_bp.get_all_article_from_catalogue'))
    return render_template('/news/news_page.html', articles=articles.json())


@news_bp.route('/update', methods=['GET', 'POST'])
@login_required
def news_catalogue_update():
    form = CatalogueForm()
    if form.validate_on_submit():  # check and validate form data
        url = url_for('api_bp.create_article', _external=True)

        # create a dictionary containing both file and non-file data
        data = {
            'title': form.title.data,
            'article': form.article.data,
        }

        # check if a file was uploaded and add it to the data dictionary
        if form.image.data:
            data['image'] = (form.image.data.filename, form.image.data.stream, form.image.data.mimetype)

        # pass the data dictionary to requests.post()
        response = requests.post(url, data=data)

        if response.status_code == 200:
            flash('Article created successfully!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Could not create article.', 'error')

    return render_template('/news/news_page_update.html', form=form)




#  ###################################################### NEWS  ########################################################


@news_bp.route('/events')
def events():
    # articles = requests.get(HOST_AND_PORT + '/article') # TODO: to be replaced with the event api route
    return render_template('/news/events_page.html')
