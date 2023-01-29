from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.favorites import FavoriteSchema
from app.implemented import favorite_service

from app.service.autorization import admin_required, auth_required, get_user_id

favorites_ns = Namespace('favorites')

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)


@favorites_ns.route("/movies/")
class FavoritesView(Resource):
    """
        Методы get и post для "/favorites"
        POST favorites:
            {
                id: Int,
                title: Str,
                description: Str,
                trailer: Str,
                year: Int,
                rating: Float,
                director_id: Int,
                genre_id: Int
            }
        """
    @auth_required
    def get(self):
        """
        Получает запорос от пользователя на вывод списка favorites
        ID ползьзователя извлекается из переданного токена,
        получает список ID в таблице favorites отсортированных
        по user_id из полученного списка, формируется новый список фильмов,
        который возвращается для передачи в шаблон
        """
        head = request.headers
        user_id = get_user_id(head)
        data = {"user_id": user_id}
        favorites = favorite_service.get_all(data)
        return favorites_schema.dump(favorites), 200  # Возвращает список id, user_id, movie_id


@favorites_ns.route("/movies/<int:mid>")
class FavoriteView(Resource):
    """
    POST "/movies/<int:mid>"
    для авторизованных пользователей позволяет добавить фильм в список избранных (favorites)
    по ID =  <int:mid>. user_id извлекается из переданного токена.

    GET  "/movies/<int:mid>"
    только для пользователей с role=="admin" Получает ID фильма из <int:mid>,
    возвращает список из favorites отсортированный по movie_id,
    что позволяет получить всех пользователей, добавихших конкретный фильм в избранное

    POST "/movies/<int:mid>"
    для авторизованных пользователей удаляет данные о фильме из списока избранных.
    """

    @auth_required
    def post(self, mid: int):

        head = request.headers
        user_id = get_user_id(head)

        data = {
            "movie_id": mid,
            "user_id": user_id
                }
        favorite_service.create(data)
        return data, 200

    @admin_required
    def get(self, mid: int):

        data = {"movie_id": mid}
        favorites = favorite_service.get_all(data)
        return favorites_schema.dump(favorites), 200

    @auth_required
    def delete(self, mid:int):
        head = request.headers
        user_id = get_user_id(head)


        data = {
            "movie_id": mid,
            "user_id": user_id
        }
        favorite = favorite_service.get_one(data)
        fid = favorites_schema.dump(favorite)[0].get("id")
        favorite_service.delete(fid)
        return "Delete", 204
