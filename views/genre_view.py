from flask import request
from flask_restx import Resource, Namespace
from app.implemented import genre_service

from app.dao.model.genre import GenreSchema
from app.service.autorization import auth_required, admin_required

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route("/")
class GenreView(Resource):
    """
       Методы GET для "/genres"
       Возвразает список всех жанров из БД
       по запросу любого авторизованного пользователя.

       Метод POST позволяет добавить новый жанр.
       Доступен пользователям с role=="admin"
       Принимает данные ввиде словаря
       genre:
           {
               id: Int,
               name: Str
           }
       """
    @auth_required
    def get(self):
        page = request.args.get("page")
        data = {"page": page}
        genres = genre_service.get_all(data)
        return genres_schema.dump(genres), 200

    @admin_required
    def post(self):
        data = request.json
        genre_service.create(data)
        return "", 201


@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    """
    Метод GET для "genres/<int:uid>
    Возвращает данные о жанре по ID
    для любого авторизованного пользователя

    PATCH доступен для пользователей с role=="admin"
    Позволяет изменить данные о жанре, по ID:
    genre {
            id: Int,
            name: Str
        }

    DELETE доступен для пользователей с role=="admin"
    Удаляет запись о жанре из БД, по переданному ID
    """

    @auth_required
    def get(self, gid: int):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200

    @admin_required
    def patch(self, gid: int):
        update_rows = request.json
        update_rows["id"] = gid
        genre_service.update(update_rows)
        return "Updated", 204

    @admin_required
    def delete(self, gid:int):
        genre_service.delete(gid)
        return "Delete", 204
