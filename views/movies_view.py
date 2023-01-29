from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.movies import MovieSchema
from app.implemented import movie_service
from app.service.autorization import auth_required, admin_required

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    """
        Методы GET эндпоинт "/movies" возвращает авторизованному пользователю весь список словарей с фильмами из БД.
        Может принимать параметры:
        /movies/?status=new&page=1
            status=new - позовляет вывести фильмы по дате выхода в порядке убывания (от нового к старому)
        по умолчанию выводит в том порядке, в котором они лежат в БД
            new&page=1 - позволяет запросить постраничный вывод, число элементов POSTS_PER_PAGE = 12 - указано в app.constants.py
            director_id=1 - вернет все фильмы режиссера с ID=1
            genre_id=1 - вернет фильмы с ganre_id=1
            year=2000 - вернет фильмы, с годом выхода 2000



        POST доступен для пользоватерей с role=="admin"
        Добавляет фильм в БД из переданного словаря:
        movies:
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
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        page = request.args.get("page")
        status = request.args.get("status")

        data = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "page": page,
            "status": status
        }

        movies_data = movie_service.get_all(data)
        movies = movies_schema.dump(movies_data)
        return movies, 200

    @admin_required
    def post(self):
        data = request.json
        movie = movie_service.create(data)
        return "", 201, {"location": f"/movies/{movie.id}"}



@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    """
    GET для "movies/<int:mid>"
    вернет фильм с запрошенным ID

    PUT, PATCH только для пользователей с role=="admin"
    позволяют изменять данные фильма в БД

    DELETE только для пользователей с role=="admin"
    позволяют удалить данные о фильме из БД
    """

    @auth_required
    def get(self, mid: int):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid: int):
        update_rows = request.json
        update_rows["id"] = mid
        movie_service.update(update_rows)
        return "Updated", 204

    @admin_required
    def patch(self, mid: int):
        update_rows = request.json
        update_rows["id"] = mid
        movie_service.update(update_rows)
        return "Updated", 204

    @admin_required
    def delete(self, mid:int):
        movie_service.delete(mid)
        return "Delete", 204
