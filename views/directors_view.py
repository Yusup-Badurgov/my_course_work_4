from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.directors import DirectorSchema
from app.implemented import directors_service
from app.service.autorization import auth_required, admin_required

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route("/")
class DirectorView(Resource):
    """
    Методы GET для "/directors"
    Возвразает список всех режиссеров из БД
    по запросу любого авторизованного пользователя.

    Метод POST позволяет добавить нового режиссера.
    Доступен пользователям с role=="admin"
    Принимает данные ввиде словаря
    director:
        {
            id: Int,
            name: Str
        }
    """
    @auth_required
    def get(self):
        page = request.args.get("page")
        data = {"page": page}
        directors = directors_service.get_all(data)
        return directors_schema.dump(directors), 200

    @admin_required
    def post(self):
        data = request.json
        directors_service.create(data)
        return "", 201



@director_ns.route("/<int:uid>")
class DirectorView(Resource):
    """
    Метод GET для "directors/<int:uid>
    Возвращает данные конкретного режиссера по ID
    для любого авторизованного пользователя

    PATCH доступен для пользователей с role=="admin"
    Позволяет изменить данные режиссера, по ID:
    director {
            id: Int,
            name: Str
        }

    DELETE доступен для пользователей с role=="admin"
    Удаляет запись о режиссере из БД, по переданному ID
    """

    @auth_required
    def get(self, uid: int):
        director = directors_service.get_one(uid)
        return director_schema.dump(director), 200

    @admin_required
    def patch(self, uid: int):
        update_rows = request.json
        update_rows["id"] = uid
        directors_service.update(update_rows)
        return "Updated", 204

    @admin_required
    def delete(self, uid:int):
        directors_service.delete(uid)
        return "Delete", 204
