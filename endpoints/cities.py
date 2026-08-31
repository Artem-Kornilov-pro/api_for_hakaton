import logging
import random
from typing import Any

from fastapi import APIRouter, HTTPException

from data.cities import cities, countries, landmarks

# Настройка логирования
logger = logging.getLogger(__name__)

cities_router = APIRouter(tags=["cities"])


# Вспомогательная функция
def get_item_or_404(data_dict, item_id, item_name):
    if item_id not in data_dict:
        raise HTTPException(status_code=404, detail=f"{item_name} с ID {item_id} не найден")
    return data_dict[item_id]


# ========== ЭНДПОИНТЫ ДЛЯ СТРАН ==========


@cities_router.get("/all_countries")
async def get_all_countries():
    """Возвращает все страны"""
    logger.info("Запрос всех стран")
    return countries


@cities_router.get("/names_of_all_countries")
async def get_names_of_all_countries():
    """Возвращает названия всех стран"""
    logger.info("Запрос названий всех стран")
    return [country["name"] for country in countries.values()]


@cities_router.get("/random_country")
async def get_random_country():
    """Возвращает случайную страну"""
    country_id = random.choice(list(countries.keys()))
    logger.info(f"Случайная страна с ID: {country_id}")
    return countries[country_id]


@cities_router.get("/country/{country_id}")
async def get_country_by_id(country_id: str):
    """Возвращает страну по ID"""
    return get_item_or_404(countries, country_id, "Страна")


@cities_router.get("/country_by_name/{name}")
async def get_country_by_name(name: str):
    """Поиск страны по названию"""
    for id, country in countries.items():
        if name.lower() == country["name"].lower():
            logger.info(f"Найдена страна: {country['name']}")
            return country
    raise HTTPException(status_code=404, detail=f"Страна '{name}' не найдена")


@cities_router.get("/countries_by_continent/{continent}")
async def get_countries_by_continent(continent: str):
    """Возвращает страны по континенту"""
    result = {}
    for id, country in countries.items():
        if continent.lower() in country["continent"].lower():
            result[id] = country

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Страны на континенте '{continent}' не найдены"
        )
    logger.info(f"Запрос стран континента: {continent}")
    return result


# ========== ЭНДПОИНТЫ ДЛЯ ГОРОДОВ ==========


@cities_router.get("/all_cities")
async def get_all_cities():
    """Возвращает все города"""
    logger.info("Запрос всех городов")
    return cities


@cities_router.get("/names_of_all_cities")
async def get_names_of_all_cities():
    """Возвращает названия всех городов"""
    logger.info("Запрос названий всех городов")
    return [city["name"] for city in cities.values()]


@cities_router.get("/random_city")
async def get_random_city():
    """Возвращает случайный город"""
    city_id = random.choice(list(cities.keys()))
    logger.info(f"Случайный город с ID: {city_id}")
    return cities[city_id]


@cities_router.get("/city/{city_id}")
async def get_city_by_id(city_id: str):
    """Возвращает город по ID"""
    return get_item_or_404(cities, city_id, "Город")


@cities_router.get("/city_by_name/{name}")
async def get_city_by_name(name: str):
    """Поиск города по названию"""
    for id, city in cities.items():
        if name.lower() == city["name"].lower():
            logger.info(f"Найден город: {city['name']}")
            return city
    raise HTTPException(status_code=404, detail=f"Город '{name}' не найден")


@cities_router.get("/cities_by_country/{country}")
async def get_cities_by_country(country: str):
    """Возвращает города указанной страны"""
    result = {}
    for id, city in cities.items():
        if country.lower() == city["country"].lower():
            result[id] = city

    if not result:
        raise HTTPException(status_code=404, detail=f"Города страны '{country}' не найдены")
    logger.info(f"Запрос городов страны: {country}")
    return result


# ========== ЭНДПОИНТЫ ДЛЯ ДОСТОПРИМЕЧАТЕЛЬНОСТЕЙ ==========


@cities_router.get("/all_landmarks")
async def get_all_landmarks():
    """Возвращает все достопримечательности"""
    logger.info("Запрос всех достопримечательностей")
    return landmarks


@cities_router.get("/names_of_all_landmarks")
async def get_names_of_all_landmarks():
    """Возвращает названия всех достопримечательностей"""
    logger.info("Запрос названий всех достопримечательностей")
    return [landmark["name"] for landmark in landmarks.values()]


@cities_router.get("/random_landmark")
async def get_random_landmark():
    """Возвращает случайную достопримечательность"""
    landmark_id = random.choice(list(landmarks.keys()))
    logger.info(f"Случайная достопримечательность с ID: {landmark_id}")
    return landmarks[landmark_id]


@cities_router.get("/landmark/{landmark_id}")
async def get_landmark_by_id(landmark_id: str):
    """Возвращает достопримечательность по ID"""
    return get_item_or_404(landmarks, landmark_id, "Достопримечательность")


@cities_router.get("/landmarks_by_city/{city}")
async def get_landmarks_by_city(city: str):
    """Возвращает достопримечательности города"""
    result = {}
    for id, landmark in landmarks.items():
        if city.lower() == landmark["city"].lower():
            result[id] = landmark

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Достопримечательности в городе '{city}' не найдены"
        )
    logger.info(f"Запрос достопримечательностей города: {city}")
    return result


@cities_router.get("/landmarks_by_country/{country}")
async def get_landmarks_by_country(country: str):
    """Возвращает достопримечательности страны"""
    result = {}
    for id, landmark in landmarks.items():
        if country.lower() == landmark["country"].lower():
            result[id] = landmark

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Достопримечательности в стране '{country}' не найдены"
        )
    logger.info(f"Запрос достопримечательностей страны: {country}")
    return result


@cities_router.get("/landmarks_by_type/{type}")
async def get_landmarks_by_type(type: str):
    """Возвращает достопримечательности по типу (крепость, башня, памятник и т.д.)"""
    result = {}
    for id, landmark in landmarks.items():
        if type.lower() == landmark["type"].lower():
            result[id] = landmark

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Достопримечательности типа '{type}' не найдены"
        )
    logger.info(f"Запрос достопримечательностей типа: {type}")
    return result


# ========== ПОИСК И СТАТИСТИКА ==========


@cities_router.get("/search")
async def search_cities(query: str):
    """Поиск по всем категориям"""
    result: dict[str, dict[str, Any]] = {"countries": {}, "cities": {}, "landmarks": {}}

    # Поиск в странах
    for id, country in countries.items():
        if query.lower() in country["name"].lower() or query.lower() in country["capital"].lower():
            result["countries"][id] = country

    # Поиск в городах
    for id, city in cities.items():
        if query.lower() in city["name"].lower() or query.lower() in city["country"].lower():
            result["cities"][id] = city

    # Поиск в достопримечательностях
    for id, landmark in landmarks.items():
        if (
            query.lower() in landmark["name"].lower()
            or query.lower() in landmark["city"].lower()
            or query.lower() in landmark["country"].lower()
        ):
            result["landmarks"][id] = landmark

    total = len(result["countries"]) + len(result["cities"]) + len(result["landmarks"])
    if total == 0:
        raise HTTPException(status_code=404, detail=f"По запросу '{query}' ничего не найдено")

    logger.info(f"Поиск '{query}' дал {total} результатов")
    return result


@cities_router.get("/cities_stats")
async def get_cities_stats():
    """Статистика по базе данных"""
    stats = {
        "total_countries": len(countries),
        "total_cities": len(cities),
        "total_landmarks": len(landmarks),
        "continents": {},
        "landmark_types": {},
    }

    # Подсчет по континентам
    for country in countries.values():
        cont = country["continent"]
        stats["continents"][cont] = stats["continents"].get(cont, 0) + 1

    # Подсчет по типам достопримечательностей
    for landmark in landmarks.values():
        typ = landmark["type"]
        stats["landmark_types"][typ] = stats["landmark_types"].get(typ, 0) + 1

    logger.info("Запрос статистики")
    return stats
