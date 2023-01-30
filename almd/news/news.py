from flask import current_app
from flask import Blueprint, render_template, redirect, url_for
from factory.factory import db
from werkzeug.utils import secure_filename
from almd.forms.forms import CatalogueForm
from flask_login import login_required
from models.models import Article
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
    if form.validate_on_submit():   # check and validate form data

        file = form.image.data
        file.save(
            os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        )  # Generate path to the news static/image folder

        new_article = Article(
            title=form.title.data,
            created=date.today(),
            picture=form.image.data.filename,
            content=form.article.data  # Todo: check how to render CHKediter content on page
        )
        db.session.add(new_article)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('/news/news_page_update.html', form=form)


#  ###################################################### NEWS  ########################################################


@news_bp.route('/events')
def events():
    # articles = requests.get(HOST_AND_PORT + '/article') # TODO: to be replaced with the event api route
    return render_template('/news/events_page.html')
