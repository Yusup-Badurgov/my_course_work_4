from app.dao.favorites_dao import FavoriteDAO


class FavoriteService:
    def __init__(self, dao: FavoriteDAO):
        self.dao = dao

    def get_one(self, data):
        user_id = data.get("user_id")
        movie_id = data.get("movie_id")
        return self.dao.get_users_favorite(user_id, movie_id)

    def get_all(self, data):
        if data.get("movie_id") is not None:
            favorites = self.dao.get_by_movie_id(data.get("movie_id"))
            return favorites
        if data.get("user_id") is not None:
            favorites = self.dao.get_by_user_id(data.get("user_id"))
            return favorites

    def create(self, data):
        return self.dao.create(data)

    def delete(self, fid):
        data = self.dao.get_one(fid)
        return self.dao.delete(data)
