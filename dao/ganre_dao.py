from app.dao.model.genre import Genre

#CRUD
class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        return self.session.query(Genre).get(gid)

    def get_all(self):
        return self.session.query(Genre).all()

    def get_page(self, page, per_page):
        return self.session.query(Genre).paginate(page, per_page, True).items

    def create(self, data):
        new_genre = Genre(**data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update(self, data):
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, genre):
        self.session.delete(genre)
        self.session.commit()
