from unittest.mock import MagicMock

import pytest

from app.service.movies_service import MovieService


class TestService:
    @pytest.fixture(autouse=True)
    def movie_service(self, dao_movie):
        self.movie_service = MovieService(dao=dao_movie)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        data = {
            "director_id": None,
            "genre_id": None,
            "year": None,
            "page": None,
            "status": None
        }
        movies = self.movie_service.get_all(data)
        assert len(movies)> 0

    def test_create_movie(self):
        create_movie = {
            'id': 1,
            'title': 'Броненосец «Потемкин»',
            'description': 'Сюжет, основанный на подлинном историческом событии, '
        'образно выразил основные социальные тенденции ХХ века: '
        'массовое стремление к свободе, борьбу с тиранией, защиту человеческого достоинства, '
        'призыв к единению людей во имя равноправия. Новаторская форма фильма и сегодня оказывает глубокое '
        'влияние на развитие выразительных средств кино.',
            'trailer': 'https://www.kinopoisk.ru/film/481/',
            'year': 1925,
            'rating': 1.0,
            'genre_id': 1,
            'director_id': 1
        }
        movie = self.movie_service.create(create_movie)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)


    def test_update(self):
        movie_update = {
            'id': 1,
            'title': 'Броненосец «Потемкин»',
            'description': 'Сюжет, основанный на подлинном историческом событии, '
        'образно выразил основные социальные тенденции ХХ века: '
        'массовое стремление к свободе, борьбу с тиранией, защиту человеческого достоинства, '
        'призыв к единению людей во имя равноправия. Новаторская форма фильма и сегодня оказывает глубокое '
        'влияние на развитие выразительных средств кино.',
            'trailer': 'https://www.kinopoisk.ru/film/481/',
            'year': 1925,
            'rating': 12.0,
            'genre_id': 1,
            'director_id': 1
        }
        self.movie_service.update(movie_update)
