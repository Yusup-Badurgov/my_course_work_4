from app.dao.movie_dao import MovieDAO
from app.constants import POSTS_PER_PAGE

class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, data):
        if data.get("director_id") is not None:
            movies = self.dao.get_by_director_id(data.get("director_id"))
        elif data.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(data.get("genre_id"))
        elif data.get("year") is not None:
            movies = self.dao.get_by_year(data.get("year"))

        elif data.get("status") == "new" and data.get("page") is not None:
            per_page = POSTS_PER_PAGE
            return self.dao.get_sort_page(int(data.get("page")), per_page)
        elif data.get("page") is not None:
            per_page = POSTS_PER_PAGE
            return self.dao.get_page(int(data.get("page")), per_page)
        elif data.get("status") == "new":
            return self.dao.get_sort_all()
        else:
            movies = self.dao.get_all()
        return movies

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")
        return self.dao.update(movie)

    def update_part(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)

        if "title" in data:
            movie.title = data.get("title")
        if "description" in data:
            movie.description = data.get("description")
        if "trailer" in data:
            movie.trailer = data.get("trailer")
        if "year" in data:
            movie.year = data.get("year")
        if "rating" in data:
            movie.rating = data.get("rating")
        if "genre_id" in data:
            movie.genre_id = data.get("genre_id")
        if "director_id" in data:
            movie.director_id = data.get("director_id")
        return self.dao.update(movie)

    def delete(self, mid):
        movie = self.get_one(mid)
        return self.dao.delete(movie)
