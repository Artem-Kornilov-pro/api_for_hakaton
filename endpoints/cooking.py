import logging
import random
from typing import Any

from fastapi import APIRouter, HTTPException

from data.cooking import chefs, dishes

# Настройка логирования
logger = logging.getLogger(__name__)

cooking_router = APIRouter(tags=["cooking"])


# Вспомогательная функция для проверки существования повара
def get_chef_or_404(chef_id: str):
    if chef_id not in chefs:
        raise HTTPException(status_code=404, detail=f"Повар с ID {chef_id} не найден")
    return chefs[chef_id]


# Вспомогательная функция для проверки существования блюда
def get_dish_or_404(dish_id: str):
    if dish_id not in dishes:
        raise HTTPException(status_code=404, detail=f"Блюдо с ID {dish_id} не найдено")
    return dishes[dish_id]


# ========== ЭНДПОИНТЫ ДЛЯ ПОВАРОВ ==========


# Простые эндпоинты
@cooking_router.get("/all_chef")
async def all_chef():
    """
    Простой эндпоинт: информация обо всех шеф-поварах
    """
    logger.info("Запрос всех поваров")
    return chefs


@cooking_router.get("/names_of_all_chefs")
async def get_names_of_all_chefs():
    """
    Возвращает имена всех шеф-поваров
    """
    logger.info("Запрос имён всех поваров")
    return [chef["name"] for chef in chefs.values()]


@cooking_router.get("/random_chef")
async def random_chef():
    """
    Простой эндпоинт: информация о случайном шеф-поваре
    """
    chef_id = random.choice(list(chefs.keys()))
    logger.info(f"Случайный повар с ID: {chef_id}")
    return chefs[chef_id]


# Сложные эндпоинты для поваров
@cooking_router.get("/chef/{chef_id}")
async def get_chef_by_id(chef_id: str):
    """
    Сложный эндпоинт: информация о конкретном поваре по ID
    """
    return get_chef_or_404(chef_id)


@cooking_router.get("/chef/born_after/{year}")
async def get_chefs_born_after(year: int):
    """
    Сложный эндпоинт: повара, родившиеся после указанного года
    """
    result = {chef_id: chef for chef_id, chef in chefs.items() if chef["birth_year"] > year}
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Повары, родившиеся после {year} года, не найдены"
        )
    logger.info(f"Запрос поваров, родившихся после {year}")
    return result


@cooking_router.get("/chef/by_restaurant/{restaurant}")
async def get_chefs_by_restaurant(restaurant: str):
    """
    Сложный эндпоинт: повара, работающие в указанном ресторане
    """
    result: dict[str, Any] = {}
    for chef_id, chef in chefs.items():
        if any(restaurant.lower() in r.lower() for r in chef["restaurants"]):
            result[chef_id] = chef

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Повары, работающие в ресторане '{restaurant}', не найдены"
        )
    logger.info(f"Запрос поваров ресторана: {restaurant}")
    return result


# ========== ЭНДПОИНТЫ ДЛЯ БЛЮД ==========


# Простые эндпоинты
@cooking_router.get("/all_dishes")
async def all_dishes():
    """
    Простой эндпоинт: информация обо всех блюдах
    """
    logger.info("Запрос всех блюд")
    return dishes


@cooking_router.get("/names_of_all_dishes")
async def get_names_of_all_dishes():
    """
    Простой эндпоинт: названия всех блюд
    """
    logger.info("Запрос названий всех блюд")
    return [dish["name"] for dish in dishes.values()]


@cooking_router.get("/random_dish")
async def random_dish():
    """
    Простой эндпоинт: информация о случайном блюде
    """
    dish_id = random.choice(list(dishes.keys()))
    logger.info(f"Случайное блюдо с ID: {dish_id}")
    return dishes[dish_id]


# Сложные эндпоинты для блюд
@cooking_router.get("/dish/{dish_id}")
async def get_dish_by_id(dish_id: str):
    """
    Сложный эндпоинт: информация о конкретном блюде по ID
    """
    return get_dish_or_404(dish_id)


@cooking_router.get("/dishes/by_type/{dish_type}")
async def get_dishes_by_type(dish_type: str):
    """
    Сложный эндпоинт: блюда по типу (суп, салат, основное блюдо, выпечка, напиток)
    """
    type_lower = dish_type.lower()
    result = {
        dish_id: dish for dish_id, dish in dishes.items() if dish["type"].lower() == type_lower
    }

    if not result:
        valid_types = set(d["type"] for d in dishes.values())
        raise HTTPException(
            status_code=404,
            detail=f"Блюда типа '{dish_type}' не найдены. Доступные типы: {', '.join(valid_types)}",
        )

    logger.info(f"Запрос блюд типа: {dish_type}")
    return result


@cooking_router.get("/dishes/by_country/{country}")
async def get_dishes_by_country(country: str):
    """
    Сложный эндпоинт: блюда указанной страны
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if country.lower() in dish["country"].lower()
    }

    if not result:
        raise HTTPException(status_code=404, detail=f"Блюда страны '{country}' не найдены")

    logger.info(f"Запрос блюд страны: {country}")
    return result


@cooking_router.get("/dishes/calories")
async def get_dishes_by_calories_range(min_calories: int = 0, max_calories: int = 1000):
    """
    Сложный эндпоинт: блюда в указанном диапазоне калорий
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if min_calories <= dish["calories"] <= max_calories
    }

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Блюда с калорийностью от {min_calories} до {max_calories} не найдены",
        )

    logger.info(f"Запрос блюд с калорийностью от {min_calories} до {max_calories}")
    return result


@cooking_router.get("/dishes/quick")
async def get_quick_dishes(max_minutes: int = 30):
    """
    Сложный эндпоинт: быстрые блюда (время приготовления не больше указанного)
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if dish["cooking_time_minutes"] <= max_minutes
    }

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Блюда со временем приготовления до {max_minutes} минут не найдены",
        )

    logger.info(f"Запрос быстрых блюд (до {max_minutes} минут)")
    return result


@cooking_router.get("/food_info")
async def get_food_info():
    """
    Возвращает справочную информацию:
    - список всех стран, представленных в базе
    - список всех типов блюд
    - статистика по странам и типам
    """
    # Получаем уникальные страны
    countries = sorted(set(dish["country"] for dish in dishes.values()))

    # Получаем уникальные типы блюд
    dish_types = sorted(set(dish["type"] for dish in dishes.values()))

    # Считаем количество блюд по странам
    countries_count = {}
    for dish in dishes.values():
        country = dish["country"]
        countries_count[country] = countries_count.get(country, 0) + 1

    # Считаем количество блюд по типам
    types_count = {}
    for dish in dishes.values():
        dish_type = dish["type"]
        types_count[dish_type] = types_count.get(dish_type, 0) + 1

    return {
        "countries": countries,
        "dish_types": dish_types,
        "statistics": {
            "total_dishes": len(dishes),
            "by_country": countries_count,
            "by_type": types_count,
        },
    }
