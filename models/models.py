from datetime import datetime
from factory.factory import db
from flask_login import UserMixin


def formatted_time():
    return datetime.utcnow().strftime("%Y-%m-%d")


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=formatted_time)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    picture = db.Column(db.String(500), nullable=False)
    # image =  db.relationship('Image',backref = 'article')


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return "Article database"


# class Image(db.model):
#     id =  db.Column(db.Integer, primary_key=True)
#     iamgeName = db.Column(db.String(5000), nullable=False)
#     ArticleId = db.Column(db.Integer,db.ForeignKey('Article.id'), nullable=True)

