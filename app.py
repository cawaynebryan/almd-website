from flask import Flask, render_template
from flask_ckeditor import CKEditor
from factory.factory import db
from api.api import api_bp
from almd.news.news import news_bp
from almd.about_us.about_us import about_bp
from almd.resources.resources import resources_bp


import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'change me before production'  # TODO: To be change and store in environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)    # Bind database to current flask app
ckeditor = CKEditor(app)   # instantiate CKEditor onto the flask app
app.register_blueprint(about_bp, url_prefix='')
app.register_blueprint(news_bp, url_prefix='')
app.register_blueprint(resources_bp, url_prefix='')
app.register_blueprint(api_bp, url_prefix='')


app.config['UPLOAD_FOLDER'] = 'static/images'  # configure static files url for uploading images


ADDRESS = 'http://127.0.0.1'
PORT = 5000
HOST_AND_PORT = f'{ADDRESS}:{PORT}'


with app.app_context():  # Create database with context manager if not exist
    db.create_all()


@app.route('/')
def home_page():
   # response = requests.get(HOST_AND_PORT + '/article')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
