from datetime import datetime
from factory.factory import db


def formatted_time():
    return datetime.utcnow().strftime("%Y-%m-%d")


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=formatted_time)
    title = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(5000), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return "Article database"
