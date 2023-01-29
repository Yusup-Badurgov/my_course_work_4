from app.dao.model.directors import Director
from flask_sqlalchemy import Pagination

#CRUD
class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(Director).get(uid)

    def get_all(self):
        return self.session.query(Director).all()

    def get_page(self, page, per_page):
        return self.session.query(Director).paginate(page, per_page, True).items


    def create(self, data):
        new_director = Director(**data)
        self.session.add(new_director)
        self.session.commit()
        return new_director

    def update(self, director):
        self.session.add(director)
        self.session.commit()
        return director


    def delete(self, director):
        self.session.delete(director)
        self.session.commit()
