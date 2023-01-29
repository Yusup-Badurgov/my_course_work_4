from app.dao.model.users import User

#CRUD
class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, user):
        self.session.add(user)
        self.session.commit()
        return user


    def delete(self, user):
        self.session.delete(user)
        self.session.commit()


    def get_users(self, email, user_password):
        users = User.query.filter(User.email == email).filter(User.password == user_password)
        return users

    def get_by_email(self, data):
        return self.session.query(User).filter(User.email == data).all()
