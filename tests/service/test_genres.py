from unittest.mock import MagicMock

import pytest

from app.service.genre_service import GenreService


class TestService:

    @pytest.fixture(autouse=True)
    def genre_service(self, dao_genre):
        self.genre_service = GenreService(dao=dao_genre)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre.id is not None
        assert genre is not None

    def tes_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres)>0

    def test_create(self):
        create_genre = {'id': 1, 'name': 'комедия'}
        genre = self.genre_service.create(create_genre)
        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_update = {'id': 1, 'name': 'Документальное'}
        self.genre_service.update(genre_update)
