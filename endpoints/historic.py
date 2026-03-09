from fastapi import APIRouter, HTTPException
import logging
import random
from typing import Dict, List, Optional

# Настройка логирования
logger = logging.getLogger(__name__)

historic_router = APIRouter(tags=["historic"])

# Расширенная база исторических фактов
historic_facts = {
    "1": {
        "year": 1200, 
        "title": "BMW в Египте",
        "fact": "BMW не ездили по Египту", 
        "description": "В 1200 году в Египте правили мамлюки, и конечно же, никаких автомобилей тогда не существовало.",
        "img_url": "https://avatars.mds.yandex.net/i?id=8238cb89d8df1a7e258957fe6ddbf195_l-9053276-images-thumbs&n=13"
    },
    "2": {
        "year": 1380,
        "title": "Куликовская битва",
        "fact": "Куликовская битва",
        "description": "Сражение между русскими войсками под предводительством Дмитрия Донского и монголо-татарскими войсками Мамая.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1974877/1250098087/S600xU_2x"
    },
    "3": {
        "year": 862,
        "title": "Призвание варягов",
        "fact": "Начало династии Рюриковичей",
        "description": "Славянские племена призвали варягов для княжения, что считается началом российской государственности.",
        "img_url": "https://avatars.mds.yandex.net/i?id=db17c5eb65bbfd029da6931a647acf44_sr-5302491-images-thumbs&n=13"
    },
    "4": {
        "year": 988,
        "title": "Крещение Руси",
        "fact": "Владимир Красное Солнышко крестил Русь",
        "description": "Князь Владимир принял христианство и крестил Киевскую Русь, что определило культурное развитие страны на века.",
        "img_url": "https://media.pravoslavie.ru/469808.s.jpg"
    },
    "5": {
        "year": 1240,
        "title": "Невская битва",
        "fact": "Александр Невский разбил шведов",
        "description": "Молодой князь Александр Ярославич одержал победу над шведским войском, получив прозвище 'Невский'.",
        "img_url": "https://cdn.tvspb.ru/storage/wp-content/uploads/2022/06/p1bkmmyzsmdthumbnail_rAszbEG.jpg__0_0x0.jpg"
    },
    "6": {
        "year": 1703,
        "title": "Основание Санкт-Петербурга",
        "fact": "Петр I основал новую столицу",
        "description": "Петр Первый заложил Петропавловскую крепость, с чего началось строительство Санкт-Петербурга.",
        "img_url": "https://avatars.mds.yandex.net/i?id=86b6972d54c96ea9927fa5e971e069e19b85f636-4719550-images-thumbs&n=13"
    },
    "7": {
        "year": 1812,
        "title": "Бородинское сражение",
        "fact": "Крупнейшее сражение Отечественной войны 1812 года",
        "description": "Генеральное сражение между русской армией Кутузова и французской армией Наполеона под Москвой.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2038203/1237550538/S600xU_2x"
    },
    "8": {
        "year": 1861,
        "title": "Отмена крепостного права",
        "fact": "Александр II освободил крестьян",
        "description": "Император Александр II подписал манифест об отмене крепостного права в России.",
        "img_url": "https://i0.wp.com/gsrussia.ru/wp-content/uploads/2022/12/image-16.png"
    },
    "9": {
        "year": 1961,
        "title": "Первый полет в космос",
        "fact": "Гагарин стал первым человеком в космосе",
        "description": "Юрий Гагарин на корабле 'Восток-1' совершил первый в истории полет в космическое пространство.",
        "img_url": "https://rgantd.ru/upload/resize_cache/iblock/3e9/500_500_1/3lucha9bdp06bjvu71rbizts562vj7hs.jpg"
    },
    "10": {
        "year": 1945,
        "title": "День Победы",
        "fact": "Окончание Великой Отечественной войны",
        "description": "Подписание акта о безоговорочной капитуляции Германии ознаменовало победу СССР в войне.",
        "img_url": "https://avatars.mds.yandex.net/i?id=2c7291cb637dd5c15aa770fa60c61d852be09bb0-5865432-images-thumbs&n=13"
    }
}

# Новая база данных о правителях
rulers = {
    "1": {
        "name": "Рюрик",
        "years_rule": "862-879",
        "dynasty": "Рюриковичи",
        "facts": ["Основатель династии Рюриковичей", "Первый новгородский князь", "Призван на княжение славянскими племенами"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/5528860/1248304069/S600xU_2x",
        "important_event": "Призвание варягов и начало княжения в Новгороде"
    },
    "2": {
        "name": "Владимир Святославич (Красное Солнышко)",
        "years_rule": "980-1015",
        "dynasty": "Рюриковичи",
        "facts": ["Крестил Русь в 988 году", "Объединил все восточнославянские земли", "При нем началась чеканка монет"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2223725/1174719715/S600xU_2x",
        "important_event": "Крещение Руси"
    },
    "3": {
        "name": "Ярослав Мудрый",
        "years_rule": "1019-1054",
        "dynasty": "Рюриковичи",
        "facts": ["Составил первый свод законов 'Русская правда'", "При нем Киев стал одним из крупнейших городов Европы", "Основал библиотеку в Софийском соборе"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/4785917/1245008196/S600xU_2x",
        "important_event": "Расцвет Киевской Руси и создание 'Русской правды'"
    },
    "4": {
        "name": "Александр Невский",
        "years_rule": "1252-1263",
        "dynasty": "Рюриковичи",
        "facts": ["Победил шведов в Невской битве (1240)", "Разбил немецких рыцарей в Ледовом побоище (1242)", "Причислен к лику святых"],
        "img_url": "https://www.pravmir.ru/wp-content/uploads/2012/09/826_59-768x995.jpeg",
        "important_event": "Защита северо-западных рубежей Руси от крестоносцев"
    },
    "5": {
        "name": "Иван III Васильевич",
        "years_rule": "1462-1505",
        "dynasty": "Рюриковичи",
        "facts": ["Сверг монголо-татарское иго (1480)", "Принял титул 'Государь всея Руси'", "Построил Московский Кремль из красного кирпича"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/5504037/1237254929/S600xU_2x",
        "important_event": "Стояние на реке Угре - конец ордынского ига"
    },
    "6": {
        "name": "Иван IV Грозный",
        "years_rule": "1533-1584",
        "dynasty": "Рюриковичи",
        "facts": ["Первый венчанный на царство царь (1547)", "Присоединил Казанское и Астраханское ханства", "Начало освоения Сибири"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/10843572/1244157545/S600xU_2x",
        "important_event": "Венчание на царство и начало реформ"
    },
    "7": {
        "name": "Петр I Великий",
        "years_rule": "1682-1725",
        "dynasty": "Романовы",
        "facts": ["Провел масштабные реформы", "Основал Санкт-Петербург", "Создал российский флот", "Провел губернскую реформу"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2114485/1247603534/S600xU_2x",
        "important_event": "Основание Санкт-Петербурга и провозглашение России империей"
    },
    "8": {
        "name": "Екатерина II Великая",
        "years_rule": "1762-1796",
        "dynasty": "Романовы",
        "facts": ["Присоединила Крым и Новороссию", "Провела губернскую реформу", "Основала Эрмитаж", "Переписывалась с Вольтером"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2368666/1237485367/S600xU_2x",
        "important_event": "Присоединение Крыма и развитие просвещения"
    },
    "9": {
        "name": "Александр II Освободитель",
        "years_rule": "1855-1881",
        "dynasty": "Романовы",
        "facts": ["Отменил крепостное право (1861)", "Провел военную реформу", "Продал Аляску США (1867)"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2363292/1247705158/S600xU_2x",
        "important_event": "Отмена крепостного права"
    },
    "10": {
        "name": "Николай II",
        "years_rule": "1894-1917",
        "dynasty": "Романовы",
        "facts": ["Последний российский император", "Отрекся от престола в 1917 году", "Расстрелян с семьей в 1918 году"],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2295215/1247693461/S600xU_2x",
        "important_event": "Февральская революция и отречение от престола"
    }
}

# Эндпоинты для исторических фактов
@historic_router.get("/facts")
async def get_all_facts():
    """
    Возвращает все исторические факты
    """
    logger.info("Запрос всех исторических фактов")
    return historic_facts

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
    dynasty_rulers = {id: ruler for id, ruler in rulers.items() if ruler["dynasty"].lower() == dynasty.lower()}
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
    stats = {
        "total_facts": len(historic_facts),
        "total_rulers": len(rulers),
        "facts_years": sorted(set(fact["year"] for fact in historic_facts.values())),
        "dynasties": {
            "ryurikovichi": len([r for r in rulers.values() if r["dynasty"] == "Рюриковичи"]),
            "romanovy": len([r for r in rulers.values() if r["dynasty"] == "Романовы"])
        }
    }
    logger.info("Запрос статистики")
    return stats

