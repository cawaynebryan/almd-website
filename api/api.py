from flask import Blueprint, jsonify, request
from factory.factory import db
from models.models import Article



api_bp = Blueprint('api_bp', __name__, url_prefix='')
API_KEY_ = 'topsecretapikey'


# Get request  
#  /article --> fetch all article
@api_bp.route('/article')
def get_all_article_from_catalogue():
    articles = db.session.query(Article).all()
    return jsonify(articles=[article.to_dict() for article in articles])


# /article/jack-bauer --> fetch the article on jack-bauer
@api_bp.route('/article/<int:id>')
def get_article_by_id(id):
    print(id)
    try:
        article = db.get_or_404(Article, id)
        return jsonify(article=article.to_dict())
    except:
        return jsonify(error={'failure': 'Something went wrong! could not fetch the targeted article.'}), 404


# return
@api_bp.route('/frequent')
def most_recent_article():  # Query for the most recent article
    recent_article = db.session.query(Article)[-5:]  # slicing is used to return the last five element in the list
    return jsonify(article=[articles.to_dict() for articles in recent_article])


# Post request
# /article --> create one new article
@api_bp.route('/article', methods=['POST'])  # TODO: check if db exist if not create db
def create_article():
    new_article = Article(title='Web dev', picture='Cawayne', content='The brain behind this website')
    # TODO: Information should come from form
    try:
        db.session.add(new_article)
        db.session.commit()
        return jsonify(respose={'success': 'successfully added new article'})   # TODO: add conditional in case of failure
    except:
        return jsonify(error={'failure': 'Something went wrong! could not create the article.'}), 404


# Put request
# /article/jack-bauer --> update the article on jack-bauer
@api_bp.route('/article/<int:id>')
def replace_article_by_id(id):
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if api_key:
            selected_article = db.get_or_404(Article, id)
            selected_article.title = 'New title goes here'
            selected_article.picture = 'New content goes here'
            selected_article.content = 'This is where the new article content goes'
            db.session.add(selected_article)
            db.session.commit()
            return jsonify(response={'success': 'Successfully updated the article in the catalogue'}), 200
        else:
            return jsonify(
                error={'failure': 'Something went wrong! could not replace the article in the catalogue.'}), 404
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403


# Patch request
# /article/jack-bauer --> update the article on jack-bauer 
# TODO: add a patch route


# /article --> delete all article
@api_bp.route('/article', methods=['DELETE'])
def delete_article_catalogue():
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        try:
            num_rows_deleted = db.session.query(Article).delete()
            print(f"The total number of rows delete: {num_rows_deleted}")
            db.session.commit()
            return jsonify(response={'success': 'successfully deleted all the article form the database'}), 200
        except:
            db.session.rollback()
            return jsonify(
                error={'failure': 'Something went wrong! could not delete the articles in the catalogue'}), 404
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403


# /article/jack-bauer --> delete a specific article base on the id provided
@api_bp.route('/article/<int:id>', methods=['DELETE'])
def delete_article_by_id(id):
    print(id)
    article = db.get_or_404(Article, id)
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if article:
            db.session.delete(article)
            db.session.commit()
            return jsonify(response={'success': f'successfully deleted article with id:{article.id} '
                                                f'from the article form the database'}), 200
        else:
            db.session.rollback()
            return jsonify(error={"failure": "Sorry an article with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403
