import logging
import random

from fastapi import APIRouter, HTTPException

from data.historic import historic_facts, rulers

# Настройка логирования
logger = logging.getLogger(__name__)

historic_router = APIRouter(tags=["historic"])


# Эндпоинты для исторических фактов
@historic_router.get("/facts")
async def get_all_facts():
    """
    Возвращает все исторические факты
    """
    logger.info("Запрос всех исторических фактов")
    return historic_facts

@historic_router.get("/titles_of_facts")
async def get_all_titles_of_facts():
    """
    Возвращает названия всех исторических фактов
    """
    logger.info("Запрос заголовков всех историчнских фактов")
    return [ fact["title"] for fact in historic_facts.values()]

@historic_router.get("/facts/{fact_id}")
async def get_fact_by_id(fact_id: str):
    """
    Возвращает конкретный исторический факт по ID
    """
    if fact_id not in historic_facts:
        raise HTTPException(status_code=404, detail="Факт не найден")
    logger.info(f"Запрос факта с ID: {fact_id}")
    return historic_facts[fact_id]


@historic_router.get("/random_fact")
async def get_random_fact():
    """
    Возвращает случайный исторический факт
    """
    fact_id = random.choice(list(historic_facts.keys()))
    logger.info(f"Случайный факт с ID: {fact_id}")
    return historic_facts[fact_id]


@historic_router.get("/facts/year/{year}")
async def get_facts_by_year(year: int):
    """
    Возвращает все факты за указанный год
    """
    facts_in_year = {id: fact for id, fact in historic_facts.items() if fact["year"] == year}
    if not facts_in_year:
        raise HTTPException(status_code=404, detail=f"Факты за {year} год не найдены")
    logger.info(f"Запрос фактов за {year} год")
    return facts_in_year


# Эндпоинты для правителей
@historic_router.get("/rulers")
async def get_all_rulers():
    """
    Возвращает всех правителей
    """
    logger.info("Запрос всех правителей")
    return rulers

@historic_router.get("/names_of_rulers")
async def get_names_all_rullers():
    """
    Возвращает имена всех правителей
    """
    logger.info("Имён всех правителей")
    return [ ruler["name"] for ruler in rulers.values()]

@historic_router.get("/rulers/{ruler_id}")
async def get_ruler_by_id(ruler_id: str):
    """
    Возвращает информацию о конкретном правителе по ID
    """
    if ruler_id not in rulers:
        raise HTTPException(status_code=404, detail="Правитель не найден")
    logger.info(f"Запрос правителя с ID: {ruler_id}")
    return rulers[ruler_id]


@historic_router.get("/rulers/dynasty/{dynasty}")
async def get_rulers_by_dynasty(dynasty: str):
    """
    Возвращает всех правителей указанной династии (Рюриковичи или Романовы)
    """
    dynasty_rulers = {
        id: ruler for id, ruler in rulers.items() if ruler["dynasty"].lower() == dynasty.lower()
    }
    if not dynasty_rulers:
        raise HTTPException(status_code=404, detail=f"Правители династии {dynasty} не найдены")
    logger.info(f"Запрос правителей династии: {dynasty}")
    return dynasty_rulers


@historic_router.get("/random_ruler")
async def get_random_ruler():
    """
    Возвращает случайного правителя
    """
    ruler_id = random.choice(list(rulers.keys()))
    logger.info(f"Случайный правитель с ID: {ruler_id}")
    return rulers[ruler_id]


@historic_router.get("/stats")
async def get_stats():
    """
    Возвращает статистику по базе данных
    """
    # Подсчёт правителей по династиям/эпохам
    dynasties_count = {}
    for ruler in rulers.values():
        dynasty = ruler["dynasty"]
        dynasties_count[dynasty] = dynasties_count.get(dynasty, 0) + 1

    # Самый старый и самый новый факт
    facts_list = list(historic_facts.values())
    oldest_fact = min(facts_list, key=lambda x: x["year"]) if facts_list else None
    newest_fact = max(facts_list, key=lambda x: x["year"]) if facts_list else None

    # Самый старый и самый новый правитель (по началу правления)
    rulers_list = list(rulers.values())

    # Функция для извлечения года начала правления
    def get_start_year(ruler):
        try:
            return int(ruler["years_rule"].split("-")[0])
        except (ValueError, KeyError, AttributeError):
            return 0

    oldest_ruler = min(rulers_list, key=get_start_year) if rulers_list else None
    newest_ruler = max(rulers_list, key=get_start_year) if rulers_list else None

    stats = {
        "total_facts": len(historic_facts),
        "total_rulers": len(rulers),
        "facts_years": {
            "min": min(fact["year"] for fact in historic_facts.values()),
            "max": max(fact["year"] for fact in historic_facts.values()),
            "all": sorted(set(fact["year"] for fact in historic_facts.values())),
        },
        "rulers_by_dynasty": dynasties_count,
        "oldest_fact": {
            "title": oldest_fact["title"] if oldest_fact else None,
            "year": oldest_fact["year"] if oldest_fact else None,
        },
        "newest_fact": {
            "title": newest_fact["title"] if newest_fact else None,
            "year": newest_fact["year"] if newest_fact else None,
        },
        "oldest_ruler": {
            "name": oldest_ruler["name"] if oldest_ruler else None,
            "start_year": get_start_year(oldest_ruler) if oldest_ruler else None,
        },
        "newest_ruler": {
            "name": newest_ruler["name"] if newest_ruler else None,
            "start_year": get_start_year(newest_ruler) if newest_ruler else None,
        },
    }

    logger.info("Запрос статистики")
    return stats
