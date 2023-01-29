from app.dao.directors_dao import DirectorDAO
from flask_sqlalchemy import Pagination
from app.constants import POSTS_PER_PAGE


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self, data):
        if data.get("page") is not None:
            per_page = POSTS_PER_PAGE
            return self.dao.get_page(int(data.get("page")), per_page)
        else:
            return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        uid = data.get("id")
        director = self.get_one(uid)
        director.name = data.get("name")
        return self.dao.update(director)

    def update_part(self, data):
        uid = data.get("id")
        director = self.get_one(uid)
        if "name" in data:
            director.name = data.get("name")
        return self.dao.update(director)

    def delete(self, uid):
        director = self.get_one(uid)
        return self.dao.delete(director)
