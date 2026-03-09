from fastapi import APIRouter, HTTPException
import logging
import random
from typing import Optional

# Настройка логирования
logger = logging.getLogger(__name__)

movies_router = APIRouter(tags=["movies"])

# База данных фильмов
movies = {
    "1": {
        "title": "Иван Васильевич меняет профессию",
        "year": 1973,
        "director": "Леонид Гайдай",
        "genre": "Комедия",
        "description": "Инженер Тимофеев изобретает машину времени и отправляет своего управдома в эпоху Ивана Грозного. Тем временем царь попадает в современную Москву.",
        "rating": 8.8,
        "actors": ["Александр Демьяненко", "Юрий Яковлев", "Леонид Куравлёв", "Наталья Селезнёва"],
        "img_url": "https://avatars.mds.yandex.net/i?id=24cb16997abc785b2b3d5be5865ab70a7cf0f84d-9229279-images-thumbs&n=13"
    },
    "2": {
        "title": "Брат",
        "year": 1997,
        "director": "Алексей Балабанов",
        "genre": "Драма",
        "description": "Демобилизованный из армии Данила Багров возвращается в родной город и пытается найти свое место в жизни. По воле обстоятельств он становится наемным убийцей.",
        "rating": 8.5,
        "actors": ["Сергей Бодров мл.", "Виктор Сухоруков", "Светлана Письмиченко", "Мария Жукова"],
        "img_url": "https://avatars.mds.yandex.net/i?id=f1e93d9ad52561d1fba77488108a47ed06a85897-5478197-images-thumbs&n=13"
    },
    "3": {
        "title": "Операция Ы и другие приключения Шурика",
        "year": 1965,
        "director": "Леонид Гайдай",
        "genre": "Комедия",
        "description": "Три новеллы о приключениях студента Шурика: на стройке, в транспорте и борьба с хулиганом Федей.",
        "rating": 8.7,
        "actors": ["Александр Демьяненко", "Наталья Селезнёва", "Юрий Никулин", "Евгений Моргунов"],
        "img_url": "https://avatars.mds.yandex.net/i?id=3efe696e7eba86f0085ef1d307c89b404ea48e11-10812270-images-thumbs&n=13"
    },
    "4": {
        "title": "Москва слезам не верит",
        "year": 1979,
        "director": "Владимир Меньшов",
        "genre": "Мелодрама",
        "description": "История трех подруг, приехавших покорять Москву. Главная героиня через 20 лет становится директором комбината и встречает свою любовь.",
        "rating": 8.3,
        "actors": ["Вера Алентова", "Ирина Муравьёва", "Алексей Баталов", "Раиса Рязанова"],
        "img_url": "https://avatars.mds.yandex.net/i?id=2a0000019ccd97e042f23db2b5f479fdd446-1544156-fast-images&n=13"
    },
    "5": {
        "title": "Кавказская пленница",
        "year": 1966,
        "director": "Леонид Гайдай",
        "genre": "Комедия",
        "description": "Студент Шурик отправляется на Кавказ собирать фольклор и попадает в водоворот событий, связанных с похищением девушки.",
        "rating": 8.6,
        "actors": ["Александр Демьяненко", "Наталья Варлей", "Юрий Никулин", "Георгий Вицин"],
        "img_url": "https://avatars.mds.yandex.net/i?id=422ead439eb51790be0abed06277d5fd8de97578-9049620-images-thumbs&n=13"
    }
}

# База данных режиссёров
directors = {
    "1": {
        "name": "Леонид Гайдай",
        "birth_year": 1923,
        "death_year": 1993,
        "best_movies": ["Операция Ы", "Кавказская пленница", "Иван Васильевич меняет профессию", "Бриллиантовая рука"],
        "bio": "Леонид Иович Гайдай — советский и российский кинорежиссёр, сценарист, актёр. Народный артист СССР. Создатель лучших советских комедий, многие фразы из которых стали крылатыми.",
        "img_url": "https://avatars.mds.yandex.net/i?id=8be00faca2f21e893e38ed1b45dd86c856508a5f-5114744-images-thumbs&n=13"
    },
    "2": {
        "name": "Алексей Балабанов",
        "birth_year": 1959,
        "death_year": 2013,
        "best_movies": ["Брат", "Брат 2", "Война", "Жмурки"],
        "bio": "Алексей Октябринович Балабанов — российский кинорежиссёр, сценарист и продюсер. Создатель культовых фильмов 1990-х и 2000-х годов, отразивших дух своего времени.",
        "img_url": "https://avatars.mds.yandex.net/i?id=9372cc118e6008b4cee7ff2f715992c89288b306-4971443-images-thumbs&n=13"
    },
    "3": {
        "name": "Владимир Меньшов",
        "birth_year": 1939,
        "death_year": 2021,
        "best_movies": ["Москва слезам не верит", "Любовь и голуби", "Ширли-мырли"],
        "bio": "Владимир Валентинович Меньшов — советский и российский актёр, кинорежиссёр, сценарист, продюсер. Обладатель премии «Оскар» за фильм «Москва слезам не верит».",
        "img_url": "https://avatars.mds.yandex.net/i?id=ec07d161b3bc930af48594b3f0294f42e4caf0ce-5291460-images-thumbs&n=13"
    },
    "4": {
        "name": "Эльдар Рязанов",
        "birth_year": 1927,
        "death_year": 2015,
        "best_movies": ["Ирония судьбы", "Служебный роман", "Гараж", "Вокзал для двоих"],
        "bio": "Эльдар Александрович Рязанов — советский и российский кинорежиссёр, сценарист, актёр, поэт. Народный артист СССР. Создатель любимых новогодних фильмов.",
        "img_url": "https://avatars.mds.yandex.net/i?id=19e5ce1a4e7176375b2bc4b930df3e2e85d64bdf-10814799-images-thumbs&n=13"
    },
    "5": {
        "name": "Никита Михалков",
        "birth_year": 1945,
        "best_movies": ["Свой среди чужих", "Раба любви", "Неоконченная пьеса", "Утомлённые солнцем"],
        "bio": "Никита Сергеевич Михалков — российский кинорежиссёр, актёр, сценарист и продюсер. Обладатель «Оскара» и Гран-при Каннского кинофестиваля.",
        "img_url": "https://avatars.mds.yandex.net/i?id=750c6e2b0a08ff8e0900500fd628606ca285efe5-6003430-images-thumbs&n=13"
    }
}

# База данных актёров
actors = {
    "1": {
        "name": "Александр Демьяненко",
        "birth_year": 1937,
        "death_year": 1999,
        "famous_roles": ["Шурик в комедиях Гайдая", "роли в фильмах 'Операция Ы', 'Кавказская пленница', 'Иван Васильевич'"],
        "bio": "Александр Сергеевич Демьяненко — советский и российский актёр театра и кино. Народный артист РСФСР. Наибольшую известность получил как исполнитель роли Шурика.",
        "img_url": "https://avatars.mds.yandex.net/i?id=dd8e9cffc766d82a3390d49146cdbdb4a6d6bec4-4576178-images-thumbs&n=13"
    },
    "2": {
        "name": "Юрий Яковлев",
        "birth_year": 1928,
        "death_year": 2013,
        "famous_roles": ["Иван Васильевич Бунша / Иван Грозный", "князь Мышкин", "Ипполит в 'Иронии судьбы'"],
        "bio": "Юрий Васильевич Яковлев — советский и российский актёр театра и кино. Народный артист СССР. Снимался у Рязанова и Гайдая, создал множество ярких образов.",
        "img_url": "https://avatars.mds.yandex.net/i?id=8f19aca03cd9c37c69ef5292a964319ced75075f-10340180-images-thumbs&n=13"
    },
    "3": {
        "name": "Сергей Бодров мл.",
        "birth_year": 1971,
        "death_year": 2002,
        "famous_roles": ["Данила Багров в 'Брате'", "роли в фильмах 'Кавказский пленник', 'Восток-Запад'"],
        "bio": "Сергей Сергеевич Бодров — российский актёр, кинорежиссёр, сценарист, телеведущий. Стал культовой фигурой после выхода фильмов 'Брат' и 'Брат 2'.",
        "img_url": "https://avatars.mds.yandex.net/i?id=a5326ef3f42e8cc0074992735af4546e4ec61fe9-4827771-images-thumbs&n=13"
    },
    "4": {
        "name": "Юрий Никулин",
        "birth_year": 1921,
        "death_year": 1997,
        "famous_roles": ["Балбес в комедиях Гайдая", "роли в фильмах 'Кавказская пленница', 'Операция Ы', 'Бриллиантовая рука'"],
        "bio": "Юрий Владимирович Никулин — советский и российский актёр, клоун, телеведущий. Народный артист СССР. Легенда советского кино и цирка.",
        "img_url": "https://avatars.mds.yandex.net/i?id=6c1296ccfa21b46f1f0903489b75308016ce97e5-8906189-images-thumbs&n=13"
    },
    "5": {
        "name": "Ирина Муравьёва",
        "birth_year": 1949,
        "famous_roles": ["Людмила в 'Москва слезам не верит'", "роли в фильмах 'Карнавал', 'Самая обаятельная и привлекательная'"],
        "bio": "Ирина Вадимовна Муравьёва — советская и российская актриса театра и кино. Народная артистка РФ. Любимица миллионов зрителей.",
        "img_url": "https://avatars.mds.yandex.net/i?id=3cbd45ab1fda8fe8ab54a447122fa6eed51a85a4-4078138-images-thumbs&n=13"
        ""
    }
}

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
        raise HTTPException(status_code=404, detail=f"Фильмы с рейтингом выше {min_rating} не найдены")
    logger.info(f"Запрос фильмов с рейтингом выше {min_rating}")
    return result

# ========== ЭНДПОИНТЫ ДЛЯ РЕЖИССЁРОВ ==========

@movies_router.get("/all_directors")
async def get_all_directors():
    """Возвращает всех режиссёров"""
    logger.info("Запрос всех режиссёров")
    return directors

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
    result = {
        "movies": {},
        "directors": {},
        "actors": {}
    }
    
    # Поиск в фильмах
    for id, movie in movies.items():
        if (query.lower() in movie["title"].lower() or 
            query.lower() in movie["director"].lower() or
            any(query.lower() in actor.lower() for actor in movie["actors"])):
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
        "average_rating": sum(movie["rating"] for movie in movies.values()) / len(movies) if movies else 0
    }
    
    # Подсчет по жанрам
    for movie in movies.values():
        genre = movie["genre"]
        stats["genres"][genre] = stats["genres"].get(genre, 0) + 1
    
    logger.info("Запрос статистики по фильмам")
    return stats