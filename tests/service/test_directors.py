from unittest.mock import MagicMock

import pytest

from app.service.directors_service import DirectorService


class TestService:

    @pytest.fixture(autouse=True)
    def director_service(self, dao_director):
        self.director_service = DirectorService(dao=dao_director)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director.id is not None
        assert director is not None

    def tes_get_all(self):
        derictors = self.director_service.get_all()
        assert len(derictors)>0

    def test_create_director(self):
        create_director = {'id': 1, 'name': ' Г. Данелия'}
        director = self.director_service.create(create_director)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_update = {'id': 1, 'name': 'А. Тарковский'}
        self.director_service.update(director_update)