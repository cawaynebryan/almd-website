from flask import flash
from flask import Blueprint, render_template, redirect, url_for
from almd.forms.forms import CatalogueForm
from flask_login import login_required
import json
import requests
import os


news_bp = Blueprint(
    'news_bp', __name__, template_folder='templates',
    static_folder='static',
    static_url_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
)




# ################################################## NEWS  #############################################################


@news_bp.route('/')
def news_catalogue():
    url = url_for('api_bp.get_all_article_from_catalogue', _external=True)
    endpoint_name = 'news_catalogue'
    articles = requests.get(url, params={'endpoint_name': endpoint_name})
    return render_template('/news/news_page.html', articles=articles.json())


@news_bp.route('/update', methods=['GET', 'POST'])
@login_required
def news_catalogue_update():
    form = CatalogueForm()
    if form.validate_on_submit():  # check and validate form data
        url = url_for('api_bp.create_article', _external=True)
        cont = {'title': form.title.data, 'article': form.article.data}
        # check if a file was uploaded and add it to the files dictionary
        files = {}
        if form.image.data:
            files['image'] = (form.image.data.filename, form.image.data.stream, form.image.data.mimetype)
        # pass the data dictionary to requests.post()
        response = requests.post(url, data=cont, files=files)
        if response.status_code == 200:
            flash('Article created successfully!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Could not create article.', 'error')

    return render_template('/news/news_page_update.html', form=form)


#  ###################################################### NEWS  ########################################################

@news_bp.route('/article/<int:article_id>')  # request individual article by id from api
def git_individual_article_by_id(article_id):
    # get recent article
    frequent_article_url = url_for('api_bp.get_first_two_articles_from_catalogue', _external=True)
    frequent_article = requests.get(frequent_article_url)

    url = url_for('api_bp.get_article_by_id', id=article_id, _external=True)
    response = requests.get(url)
    return render_template('news/news_article.html', article=response.json()['article'],
                           latest_news=frequent_article.json()['articles'])


@news_bp.route('/events')
def events():
    # articles = requests.get(HOST_AND_PORT + '/article') # TODO: to be replaced with the event api route
    return render_template('/news/events_page.html')
