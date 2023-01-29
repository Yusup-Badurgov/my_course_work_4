from unittest.mock import MagicMock

import pytest

from app.service.users_service import UserService


class TestService:

    @pytest.fixture(autouse=True)
    def user_service(self, dao_user):
        self.user_service = UserService(dao=dao_user)

    def test_get_one(self):
        user = self.user_service.get_one(1)

        assert user.id is not None
        assert user is not None


    def test_get_all(self):
        users = self.user_service.get_all()
        assert len(users)>0


    def test_create(self):
        create_user = {'email': 'test@test.hot', 'password': '1234'}
        user = self.user_service.create(create_user)


    def test_delete(self):
        self.user_service.delete(1)

    def test_update(self):
        user_update = {
            'id': 1,
            'email': 'test@test.hot',
            'password': '1234',
            "name": "Admin",
            "surname": "Admon"
        }
        self.user_service.update(user_update)
