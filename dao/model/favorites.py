from marshmallow import Schema, fields
from app.setup_db import db

class Favorite(db.Model):
    """ Модель БД favorites """
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    movie = db.relationship("Movie")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")


class FavoriteSchema(Schema):
    """ CBV БД favorites """
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    movie_id = fields.Int()
    user = fields.Pluck("UserSchema", "name")
    movie = fields.Pluck("MovieSchema", "title")
