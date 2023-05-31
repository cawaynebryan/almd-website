from flask import Blueprint, jsonify, request, flash
from almd.forms.forms import CatalogueForm
from .aws import AWSFileHandler
from factory.factory import db
from models.models import Article
from datetime import date
import os
import boto3
import botocore

aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')     # TODO: to be added to aws api calls
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

s3_handler = AWSFileHandler()


def progress_callback(bytes_uploaded):
    print("{} additional bytes uploaded".format(bytes_uploaded))


api_bp = Blueprint('api_bp', __name__, url_prefix='')
API_KEY_ = 'topsecretapikey'


@api_bp.route('/articles')  # /article --> fetch all article base on endpoint name
def get_all_article_from_catalogue():
    articles = []
    endpoint_name = request.args.get('endpoint_name')
    if endpoint_name == 'news_catalogue':
        articles = db.session.query(Article).all()
    elif endpoint_name == 'event_catalogue':
        pass
        # articles = db.session.query(Events).all()
    return jsonify(articles=[article.to_dict() for article in articles])


@api_bp.route('/articles/recent')
def get_first_four_articles_from_catalogue():
    articles = db.session.query(Article).order_by(Article.created.desc()).limit(4).all()
    if articles:
        return jsonify(articles=[article.to_dict() for article in articles])
    else:
        return jsonify(error={'failure': 'Something went wrong! could not fetch the targeted article.'}), 404


@api_bp.route('/article/<int:id>')  # /article/jack-bauer --> fetch the article on jack-bauer
def get_article_by_id(id: int):
    article = db.get_or_404(Article, id)
    if article:
        return jsonify(article=article.to_dict()), 200
    else:
        return jsonify(error={'failure': 'Something went wrong! could not fetch the targeted article.'}), 404


@api_bp.route('/article', methods=['POST'])  # /article --> create one new article
def create_article():
    form = CatalogueForm()

    # File  request for image data
    image_data = request.files['image']
    image_file = image_data.stream.read()
    image_name = image_data.filename

    # Data request for article content
    article_data = request.values.to_dict()
    article_title = article_data['title']
    article_content = article_data['article']
    print(type(request.data))

    print("__________________________")
    if image_file:
        handler.put_object_from_file_stream(file_name=image_name, image_body=image_file)
        if form:
            if form.title.data: #TODO: Edit to remove erelevand data
                new_article = Article(
                    title=article_title,
                    created=date.today(),
                    picture=image_name,
                    content=article_content
                )
                db.session.add(new_article)
                db.session.commit()
                return jsonify(response={'success': 'successfully added new article'}), 200
            else:
                return jsonify(error={'failure': 'Title title field cannot be empty.'}), 404
        else:
            return jsonify(error={'failure': 'Form data is invalid.'}), 404
    else:
        return jsonify(error={'failure': 'No image file was provided.'}), 404


@api_bp.route('/article/<int:id>')  # /article/jack-bauer --> update the article on jack-bauer
def replace_article_by_id(id: int):
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


@api_bp.route('/article', methods=['DELETE'])  # /article --> delete all article
def delete_article_catalogue():
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        query = db.session.query(Article.picture).all()
        for picture in query:
            s3_handler.delete_binary_file(picture[0])
        num_rows_deleted = db.session.query(Article).delete()

        if num_rows_deleted:
            print(f"The total number of rows delete: {num_rows_deleted}")
            db.session.commit()
            return jsonify(response={'success': 'successfully deleted all the article form the database'}), 200
        else:
            db.session.rollback()
            return jsonify(
                error={'failure': 'Something went wrong! could not delete the articles in the catalogue'}), 404
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403


@api_bp.route('/article/<int:id>', methods=['DELETE'])  # /article/jack-bauer --> delete a specific article
def delete_article_by_id(id: int):
    print(id)
    article = db.get_or_404(Article, id)
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if article:
            db.session.delete(article)
            db.session.commit()
            s3_handler.delete_binary_file(article.picture)
            print(article.picture)
            print(type(article.picture))
            return jsonify(response={'success': f'successfully deleted article with id:{article.id}'
                                                f'from the article form the database'}), 200
        else:
            db.session.rollback()
            return jsonify(error={"failure": "Sorry an article with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403


@api_bp.route('/image-server/<imageName>', methods=['GET', 'POST'])
def get_image(imageName):
    """Fetch Image from image server."""
    print(imageName)
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=f'Static/{imageName}')
        return s3_object['Body'].read()

    except botocore.exceptions.ClientError as error:
        flash(f'image {imageName} was not found')
        print(f"file: {imageName} not found!")
        print(f'The error is: {error}')
        return "File Not Found"

