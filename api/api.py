from flask import Blueprint, jsonify, request, flash
from almd.forms.forms import CatalogueForm
from .aws import AWSFileHandler
from factory.factory import db
from models.models import Article
from datetime import date
import os
import boto3
import botocore
import markupsafe

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

    """_summary_
        This updates an article that is already present in the system.
        It captures what is given on a form and makes the adjustments to the article that 
        is present. 
        Also it prefills the form with the current information so that it can be used as a 
        reference for making edits.
    Returns:
        json : with the data that is fetched from the DB that is to be prefilled on the form
              for reference.
        json : success or failure message of action
    """
@api_bp.route('/article/<int:id>/update',methods = ['POST','GET'])  # /article/jack-bauer --> update the article on jack-bauer
def Update_article(id: int):
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if request.method == "POST":
            # cleanse and validifiy data from the form and use to update the article
            selected_article = db.get_or_404(Article, id).first()
            selected_article.title = markupsafe.escape(request.form['title'])
            selected_article.picture = markupsafe.escape(request.form['image'])
            selected_article.content = markupsafe.escape(request.form['article'])
            #db.session.add(selected_article)
            db.session.commit()
            return jsonify(response={'success': 'Successfully updated the article in the catalogue'}), 200
        else:
            return jsonify(
                error={'failure': 'Something went wrong! could not replace the article in the catalogue.'}), 304
    else:
        return jsonify(error={"Invalid Key": "Please enter a valid API key"}), 403


"""
BEFORE DOING SOMETHING LIKE THIS ENSURE THE 
USER CONFIRMS BY TYPING 'DELETE ALL' TO ENSURE THAT THE ACTION TO BE DONE
IS UNDERSTOOD

"""
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
    
    """_summary_
        The intention of this service is to enable the Administrator the ability to 
        remove a particular article from the catalogue 
    Returns:
        json : success message
        json : failure message
    """

@api_bp.route('/article/<int:id>/delete', methods=['DELETE'])  # /article/jack-bauer --> delete a specific article
def delete_article_by_id(id: int):
    print(id)
    article = db.get_or_404(Article, id)
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if article:
            article.isDeleted = True
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


@api_bp.route('/article/<int:id>/delete', methods=['DELETE'])  # /article/jack-bauer --> delete a specific article
def delete_article_by_id(id: int):
    print(id)
    article = db.get_or_404(Article, id)
    api_key = request.args.get('api-key')
    if api_key == API_KEY_:
        if article:
            article.isDeleted = True
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


@api_bp.route('recyleBin/article/')
def recylceBin():
     
    pass

@api_bp.route('recyleBin/article/<:id>')

@api_bp.route('recyleBin/article/<:id>/remove')


@api_bp.route('recyleBin/empty')


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

