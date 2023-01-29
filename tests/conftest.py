from unittest.mock import MagicMock

import pytest

from app.dao.movie_dao import MovieDAO
from app.dao.model.movies import Movie

from app.dao.users_dao import UserDAO
from app.dao.model.users import User

from app.dao.ganre_dao import GenreDAO
from app.dao.model.genre import Genre

from app.dao.directors_dao import DirectorDAO
from app.dao.model.directors import Director


@pytest.fixture()
def dao_movie():
    dao_movie = MovieDAO(None)

    movie_1 = Movie(
        id=1,
        title="Броненосец Потемкин",
        description="Сюжет, основанный на подлинном историческом событии, образно выразил основные социальные тенденции ХХ века: "
                    "массовое стремление к свободе, борьбу с тиранией, защиту человеческого достоинства, призыв к единению людей во имя равноправия. "
                    "Новаторская форма фильма и сегодня оказывает глубокое влияние на развитие выразительных средств кино.",
        trailer='https://www.kinopoisk.ru/film/481/',
        year=1925,
        rating=1.0,
        genre_id=1,
        director_id=1
    )

    movie_2 = Movie(
        id=2,
        title="Дорога",
        description="Фильм о нечеловеческой жестокости и человеческом страдании, о непростых отношениях немножко сумасшедшей, "
                    "немножко святой, взъерошенной, смешной, неуклюжей и нежной Джельсомины и мрачного, массивного, "
                    "грубого и звероподобного Дзампано - женщины и мужчины, совершенно чуждых друг другу, но волею судеб, неизвестно почему, оказавшихся вместе...",
        trailer="https://www.kinopoisk.ru/film/531/",
        year=1954,
        rating=18.0,
        genre_id=2,
        director_id=2
    )

    movie_3 = Movie(
        id=3,
        title="Андеграунд",
        description="Во время Второй мировой войны в Белграде подпольщики-антифашисты организовали целую фабрику по производству оружия."
                    " Война давно закончилась, а они продолжают свою деятельность. И все эти годы наверху жизнь течёт своим чередом, "
                    "а в подполье рождаются дети, которые никогда не видели солнечного света.",
        trailer="https://www.kinopoisk.ru/film/7698/",
        year=1995,
        rating=16.0,
        genre_id=2,
        director_id=3
    )

    dao_movie.get_one = MagicMock(return_value=movie_1)
    dao_movie.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    dao_movie.create = MagicMock(return_value=Movie(id=3))
    dao_movie.delete = MagicMock()
    dao_movie.update = MagicMock()

    return dao_movie

@pytest.fixture()
def dao_user():
    dao_user = UserDAO(None)

    user_1 = User(
        id = 1,
        email = "mail@test.net",
        password = "password"
    )

    user_2 = User(
        id=2,
        email = "user@mail.com",
        password = "qwerty"
    )

    user_3 = User(
        id=3,
        email = "admin@admin.com",
        password = "admin"
    )

    dao_user.get_one = MagicMock(return_value = user_1)
    dao_user.get_all = MagicMock(return_value = [user_1, user_2, user_3])
    dao_user.create = MagicMock(return_value = User(id=1))
    dao_user.delete = MagicMock()
    dao_user.update = MagicMock()

    return dao_user

@pytest.fixture()
def dao_genre():
    dao_genre = GenreDAO(None)

    genre_1 = Genre(
        id = 1,
        name = "комедия"
    )

    genre_2 = Genre(
        id=2,
        name="драма"
    )

    genre_3 = Genre(
        id=3,
        name="историческое"
    )

    dao_genre.get_one = MagicMock(return_value = genre_1)
    dao_genre.get_all = MagicMock(return_value = [genre_1, genre_2, genre_3])
    dao_genre.create = MagicMock(return_value = Genre(id=2))
    dao_genre.delete = MagicMock()
    dao_genre.update = MagicMock()

    return dao_genre

@pytest.fixture()
def dao_director():
    dao_director = DirectorDAO(None)

    director_1 = Director(
        id = 1,
        name = "Э. Рязанов"
    )

    director_2 = Director(
        id=2,
        name="А. Роу"
    )

    director_3 = Director(
        id=3,
        name="Л. Гайдай"
    )

    dao_director.get_one = MagicMock(return_value = director_1)
    dao_director.get_all = MagicMock(return_value = [director_1, director_2, director_3])
    dao_director.create = MagicMock(return_value = Director(id=2))
    dao_director.delete = MagicMock()
    dao_director.update = MagicMock()

    return dao_director

