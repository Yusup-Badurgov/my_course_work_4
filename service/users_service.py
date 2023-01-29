import calendar
import datetime
import hashlib

import jwt
from flask_restx import abort

from app.dao.users_dao import UserDAO
from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, ALGORYTHM, SECRET


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uk):
        return self.dao.get_one(uk)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        email = data.get("email")
        password = data.get("password")
        data["password"] = self.get_hash(password)
        self.dao.create(data)
        return data

    def check_email(self, data):
        email = data.get("email")
        check_email = self.dao.get_by_email(email)
        if check_email != []:
            abort(403, "email already registered")


    def update(self, data):

        uk = data.get("id")
        user = self.get_one(uk)
        if data.get("name") is not None:
            user.name = data.get("name")
        if data.get("surname") is not None:
            user.surname = data.get("surname")
        if data.get("favorite_genre") is not None:
            user.favorite_genre = data.get("favorite_genre")
        return self.dao.update(user)

    def update_part(self, data):
        uk = data.get("id")
        user = self.get_one(uk)
        password_1 = data.get("password_1")
        password_2 = data.get("password_2")
        user_password = self.get_hash(password_1)
        if user.password == user_password:
            user.password = self.get_hash(password_2)

        return self.dao.update(user)

    def delete(self, uk):
        user = self.get_one(uk)
        return self.dao.delete(user)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_token(self, data):
        token = {}

        min3 = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
        min120 = datetime.datetime.utcnow() + datetime.timedelta(minutes=120)

        data["exp"] = calendar.timegm(min3.timetuple())
        token["access_token"] = jwt.encode(data, SECRET, ALGORYTHM)

        data["exp"] = calendar.timegm(min120.timetuple())
        token["refresh_token"] = jwt.encode(data, SECRET, ALGORYTHM)

        return token

    def check_token(self, data):
        """ Проверяем  refresh_token на валидность"""

        try:
            user_data = jwt.decode(data, SECRET, ALGORYTHM)
            this_time = calendar.timegm(datetime.datetime.utcnow().timetuple())
            if user_data.get("exp") < this_time:
                return "Token time off", 419
            else:
                return self.get_token(user_data)
        except Exception:
            return "error 401", 401

    def check_tokens(self, tokens):
        """Проверяет валидность пары token_refresh, token_access.
        При успешной проверке возвращает новую пару токенов, иначе 401
        """
        try:
            token_refresh = tokens.get("refresh_token")
            token_access = tokens.get("access_token")

            refresh_data = jwt.decode(token_refresh, SECRET, ALGORYTHM)
            access_data = jwt.decode(token_refresh, SECRET, ALGORYTHM)

            this_time = calendar.timegm(datetime.datetime.utcnow().timetuple())
            if refresh_data.get("exp") < this_time and access_data.get("exp") < this_time:
                return "Token time off", 419
            else:
                return self.get_token(refresh_data)

        except Exception:
            return "error 401", 401


    def check_user(self, data):
        """ Проверяет, наличие пользователей, после фильтрации email, password,
        а так же отсутсвие, совпадений у нескольких пользователей
        email и password одновременно.
        В случае, если запись существует и соответсвует только одному пользователю возвращает

        Dict:
        access_token: STR
        refresh_token: STR
        """
        if len(data) == 1:
            return self.get_token(data[0])
        else:
            abort(401)

    def get_user(self, data):
        """
        Получает
        dict: username, password
        Отбирает пользователей из БД, фильтрует по совпадению email и hash password
        """
        email = data.get("email")
        user_password = self.get_hash(data.get("password"))
        user = self.dao.get_users(email, user_password)
        return user
