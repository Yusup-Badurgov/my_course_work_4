from app.dao.ganre_dao import GenreDAO
from app.constants import POSTS_PER_PAGE


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self, data):
        if data.get("page") is not None:
            per_page = POSTS_PER_PAGE
            return self.dao.get_page(int(data.get("page")), per_page)
        else:
            return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        gid = data.get("id")
        genre = self.get_one(gid)
        genre.name = data.get("name")
        return self.dao.update(genre)

    def update_part(self, data):
        gid = data.get("id")
        genre = self.get_one(gid)
        if "name" in data:
            genre.name = data.get("name")
        return self.dao.update(genre)

    def delete(self, gid):
        genre = self.get_one(gid)
        return self.dao.delete(genre)
