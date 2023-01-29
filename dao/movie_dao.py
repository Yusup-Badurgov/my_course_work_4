from app.dao.model.movies import Movie


#CRUD
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        movies = self.session.query(Movie).all()
        return movies

    def get_sort_all(self):
        movies = self.session.query(Movie).order_by(Movie.year.desc()).all()
        return movies

    def get_page(self, page, per_page):
        return self.session.query(Movie).paginate(page, per_page, True).items

    def get_sort_page(self, page, per_page):
        movies = self.session.query(Movie).order_by(Movie.year.desc()).paginate(page, per_page, True).items
        return movies

    def create(self, data):
        new_movie = Movie(**data)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, movie):
        self.session.delete(movie)
        self.session.commit()

    def get_by_director_id(self, uid):
        return self.session.query(Movie).filter(Movie.director_id == uid).all()

    def get_by_genre_id(self, gid):
        return self.session.query(Movie).filter(Movie.genre_id == gid).all()

    def get_by_year(self, yid):
        return self.session.query(Movie).filter(Movie.year == yid).all()
