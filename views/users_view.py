from flask import request, jsonify, abort
from flask_restx import Resource, Namespace

from app.dao.model.users import UserSchema
from app.implemented import users_service
from app.service.autorization import admin_required, auth_required, get_user_id

users_ns = Namespace('/')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route("/auth/register")
class UserView(Resource):
    """
    Метод POST
    Регистрация пользователья, принимает:
    dict {
    email: str (notnull),
    passwors: str (notnull),
    name: str,
    surname: str,
    role: str (user or admin)}

    возвращает dict данных пользователя, пароль в виде хеш

    Метод PUT
    Получает token: str, проверяет его валидность, возвращает обновленный словарь
    dict {access_token: , refresh_token: }  или 401
    """

    def post(self):
        data = request.json

        users_service.check_email(data)
        # Проверяет был ли переданнный email зарегистрирован ранее

        hash_pass = users_service.create(data)
        return hash_pass, 201

    def put(self):

        data = request.json
        return users_service.check_token(data)


@users_ns.route("/auth/login")
class UserView(Resource):
    """
    Метод POST
    Аутентификация пользователя,
    получает dict: {
                username: Str,
                password: Str
                    }
    проверяет наличие пары в БД, возвращает словарь
    dict {access_token: , refresh_token: }

    Метод PUT:
    получает пару токенов в виде словаря
    dict {access_token: , refresh_token: }
    проверяет его валидность и возвращает
    обновленный словарь {access_token: , refresh_token: }
        или 401
    """

    def post(self):
        data = request.json
        user_data = users_service.get_user(data)
        user = users_schema.dump(user_data)
        token = users_service.check_user(user)
        return token, 200

    def put(self):
        data = request.json
        return users_service.check_tokens(data)


@users_ns.route("/user/")
class UserView(Resource):
    """
    Метод GET эндпоинт "/user/"
    Проверяет валидность токена, получает ID из переданного токена
    и возвращает данные авторизованного пользователя из БД

    Метод PATH
    Позволяет изменить данные авторизованному пользователю.
    ID береться из токена, переданного при авторизации.
    Данные для изменения передаются в виде словоря:
    dict {"name": str, "surname": str, "favorite_genre": int}
    """

    @auth_required
    def get(self):
        head = request.headers
        user_id = get_user_id(head)
        user = users_service.get_one(user_id)
        return user_schema.dump(user), 200

    @auth_required
    def patch(self):
        head = request.headers
        user_id = get_user_id(head)
        try:
            update_rows = request.json
            update_rows["id"]=user_id
            users_service.update(update_rows)
            return "Updated", 204
        except Exception as error:
            print("User not found", error)
            abort(401)


@users_ns.route("/user/password")
class UserView(Resource):
    """
   Метод PUT
   Позволяет авторизованным пользователям, изменить пароль, получает пару в виде словоря:
   dict {"password_1": str, "password_2": str}
   password_1 - действующий пароль, сравнивается с хешем из БД
   password_2 - новый пароль в БД передается в хешированном виде
   ID берется из токена переданного при авторизации

    """

    @auth_required
    def put(self):
        head = request.headers
        user_id = get_user_id(head)
        try:
            update_rows = request.json
            update_rows["id"]=user_id
            users_service.update_part(update_rows)
            return "Updated", 204

        except Exception as error:
            print("User not found", error)
            abort(401)

@users_ns.route("/users/")
class UserView(Resource):
    """
    Метод GET эндпоинт /users/
    позволяет авторизованному пользователю, с role=="admin"
    просмотреть список всех зарегистрированных ранее пользователей.
    Возвращает список словарей пользователей:
    list[dict{users}]
    """
    @admin_required
    def get(self):
        users = users_service.get_all()
        return users_schema.dump(users), 200
