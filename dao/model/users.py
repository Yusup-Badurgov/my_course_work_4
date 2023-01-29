from marshmallow import Schema, fields
from app.setup_db import db


class User(db.Model):
    """ Модель БД users """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    role = db.Column(db.String(100))


class UserSchema(Schema):
    """ CBV БД user """
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()
    genre = fields.Pluck("GenreSchema", "name")
    role = fields.Str()
