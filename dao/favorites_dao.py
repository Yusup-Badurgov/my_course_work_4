from app.dao.model.favorites import Favorite

#CRUD
class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, fid):
        return self.session.query(Favorite).get(fid)

    def get_all(self):
        favorite = self.session.query(Favorite).all()
        return favorite

    def create(self, data):
        new_favorite = Favorite(**data)
        self.session.add(new_favorite)
        self.session.commit()
        return new_favorite

    def update(self, favorite):

        self.session.add(favorite)
        self.session.commit()
        return favorite

    def delete(self, data):
        self.session.delete(data)
        self.session.commit()

    def get_by_user_id(self, uid):
        return self.session.query(Favorite).filter(Favorite.user_id == uid).all()

    def get_by_movie_id(self, mid):
        return self.session.query(Favorite).filter(Favorite.movie_id == mid).all()

    def get_users_favorite(self, uid, mid):
        favorite = Favorite.query.filter(Favorite.movie_id == mid).filter(Favorite.user_id == uid)
        return favorite
