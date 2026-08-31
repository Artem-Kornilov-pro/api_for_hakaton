import logging
import random
from typing import Any

from fastapi import APIRouter, HTTPException

from data.movies import actors, directors, movies

# Настройка логирования
logger = logging.getLogger(__name__)

movies_router = APIRouter(tags=["movies"])


# Вспомогательная функция для проверки существования
def get_item_or_404(data_dict, item_id, item_name):
    if item_id not in data_dict:
        raise HTTPException(status_code=404, detail=f"{item_name} с ID {item_id} не найден")
    return data_dict[item_id]


# ========== ЭНДПОИНТЫ ДЛЯ ФИЛЬМОВ ==========


@movies_router.get("/all_movies")
async def get_all_movies():
    """Возвращает все фильмы"""
    logger.info("Запрос всех фильмов")
    return movies


@movies_router.get("/titles_of_all_movies")
async def get_titles_of_all_movies():
    """Возвращает названия всех фильмов"""
    logger.info("Запрос названий всех фильмов")
    return [movie["title"] for movie in movies.values()]


@movies_router.get("/random_movie")
async def get_random_movie():
    """Возвращает случайный фильм"""
    movie_id = random.choice(list(movies.keys()))
    logger.info(f"Случайный фильм с ID: {movie_id}")
    return movies[movie_id]


@movies_router.get("/movie/{movie_id}")
async def get_movie_by_id(movie_id: str):
    """Возвращает конкретный фильм по ID"""
    return get_item_or_404(movies, movie_id, "Фильм")


@movies_router.get("/movies_by_year/{year}")
async def get_movies_by_year(year: int):
    """Возвращает фильмы указанного года"""
    result = {id: movie for id, movie in movies.items() if movie["year"] == year}
    if not result:
        raise HTTPException(status_code=404, detail=f"Фильмы {year} года не найдены")
    logger.info(f"Запрос фильмов {year} года")
    return result


@movies_router.get("/movies_by_genre/{genre}")
async def get_movies_by_genre(genre: str):
    """Возвращает фильмы указанного жанра"""
    result = {id: movie for id, movie in movies.items() if movie["genre"].lower() == genre.lower()}
    if not result:
        raise HTTPException(status_code=404, detail=f"Фильмы жанра '{genre}' не найдены")
    logger.info(f"Запрос фильмов жанра: {genre}")
    return result


@movies_router.get("/top_movies")
async def get_top_movies(min_rating: float = 8.0):
    """Возвращает фильмы с рейтингом выше указанного (по умолчанию 8.0)"""
    result = {id: movie for id, movie in movies.items() if movie["rating"] >= min_rating}
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Фильмы с рейтингом выше {min_rating} не найдены"
        )
    logger.info(f"Запрос фильмов с рейтингом выше {min_rating}")
    return result


# ========== ЭНДПОИНТЫ ДЛЯ РЕЖИССЁРОВ ==========


@movies_router.get("/all_directors")
async def get_all_directors():
    """Возвращает всех режиссёров"""
    logger.info("Запрос всех режиссёров")
    return directors


@movies_router.get("/names_of_all_directors")
async def get_names_of_all_directors():
    """Возвращает имена всех режиссёров"""
    logger.info("Запрос имён всех режиссёров")
    return [director["name"] for director in directors.values()]


@movies_router.get("/random_director")
async def get_random_director():
    """Возвращает случайного режиссёра"""
    director_id = random.choice(list(directors.keys()))
    logger.info(f"Случайный режиссёр с ID: {director_id}")
    return directors[director_id]


@movies_router.get("/director/{director_id}")
async def get_director_by_id(director_id: str):
    """Возвращает конкретного режиссёра по ID"""
    return get_item_or_404(directors, director_id, "Режиссёр")


@movies_router.get("/director_by_name/{name}")
async def get_director_by_name(name: str):
    """Поиск режиссёра по имени"""
    for dir_id, director in directors.items():
        if name.lower() in director["name"].lower():
            logger.info(f"Найден режиссёр: {director['name']}")
            return director
    raise HTTPException(status_code=404, detail=f"Режиссёр '{name}' не найден")


# ========== ЭНДПОИНТЫ ДЛЯ АКТЁРОВ ==========


@movies_router.get("/all_actors")
async def get_all_actors():
    """Возвращает всех актёров"""
    logger.info("Запрос всех актёров")
    return actors


@movies_router.get("/names_of_all_actors")
async def get_names_of_all_actors():
    """Возвращает имена всех актёров"""
    logger.info("Запрос имён всех актёров")
    return [actor["name"] for actor in actors.values()]


@movies_router.get("/random_actor")
async def get_random_actor():
    """Возвращает случайного актёра"""
    actor_id = random.choice(list(actors.keys()))
    logger.info(f"Случайный актёр с ID: {actor_id}")
    return actors[actor_id]


@movies_router.get("/actor/{actor_id}")
async def get_actor_by_id(actor_id: str):
    """Возвращает конкретного актёра по ID"""
    return get_item_or_404(actors, actor_id, "Актёр")


@movies_router.get("/actor_by_name/{name}")
async def get_actor_by_name(name: str):
    """Поиск актёра по имени"""
    for act_id, actor in actors.items():
        if name.lower() in actor["name"].lower():
            logger.info(f"Найден актёр: {actor['name']}")
            return actor
    raise HTTPException(status_code=404, detail=f"Актёр '{name}' не найден")


# ========== ПОИСК ПО ВСЕЙ БАЗЕ ==========


@movies_router.get("/search")
async def search_all(query: str):
    """
    Поиск по всем категориям (фильмы, режиссёры, актёры)
    """
    result: dict[str, dict[str, Any]] = {"movies": {}, "directors": {}, "actors": {}}

    # Поиск в фильмах
    for id, movie in movies.items():
        if (
            query.lower() in movie["title"].lower()
            or query.lower() in movie["director"].lower()
            or any(query.lower() in actor.lower() for actor in movie["actors"])
        ):
            result["movies"][id] = movie

    # Поиск в режиссёрах
    for id, director in directors.items():
        if query.lower() in director["name"].lower():
            result["directors"][id] = director

    # Поиск в актёрах
    for id, actor in actors.items():
        if query.lower() in actor["name"].lower():
            result["actors"][id] = actor

    total_results = len(result["movies"]) + len(result["directors"]) + len(result["actors"])
    if total_results == 0:
        raise HTTPException(status_code=404, detail=f"По запросу '{query}' ничего не найдено")

    logger.info(f"Поиск по запросу '{query}' дал {total_results} результатов")
    return result


# ========== СТАТИСТИКА ==========


@movies_router.get("/movies_stats")
async def get_movies_stats():
    """Возвращает статистику по базе данных"""
    stats = {
        "total_movies": len(movies),
        "total_directors": len(directors),
        "total_actors": len(actors),
        "genres": {},
        "years": sorted(set(movie["year"] for movie in movies.values())),
        "average_rating": sum(movie["rating"] for movie in movies.values()) / len(movies)
        if movies
        else 0,
    }

    # Подсчет по жанрам
    for movie in movies.values():
        genre = movie["genre"]
        stats["genres"][genre] = stats["genres"].get(genre, 0) + 1

    logger.info("Запрос статистики по фильмам")
    return stats
