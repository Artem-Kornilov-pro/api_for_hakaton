from fastapi import APIRouter, HTTPException
import logging
import random

# Настройка логирования
logger = logging.getLogger(__name__)

cities_router = APIRouter(tags=["cities"])

# База данных стран
countries = {
    "1": {
        "name": "Россия",
        "capital": "Москва",
        "continent": "Европа/Азия",
        "population": 146000000,
        "area": 17100000,
        "fact": "Самая большая страна в мире, занимает 1/8 часть суши",
        "img_url": "https://avatars.mds.yandex.net/i?id=e00fa262711384c37796f0d9119e7f97620c5662-5482118-images-thumbs&n=13"
    },
    "2": {
        "name": "Франция",
        "capital": "Париж",
        "continent": "Европа",
        "population": 68000000,
        "area": 551695,
        "fact": "Франция - самая посещаемая страна в мире, ежегодно её посещают около 90 миллионов туристов",
        "img_url": "https://avatars.mds.yandex.net/i?id=ed496755957249f46a29ca443b56092562daa99d-5332070-images-thumbs&n=13"
    },
    "3": {
        "name": "Египет",
        "capital": "Каир",
        "continent": "Африка",
        "population": 104000000,
        "area": 1001450,
        "fact": "В Египте находится одно из семи чудес света - пирамиды Гизы",
        "img_url": "https://avatars.mds.yandex.net/i?id=872cb8a0df4aeabfdfe0c7ee2babe028b36b4227-12377907-images-thumbs&n=13"
    },
    "4": {
        "name": "Италия",
        "capital": "Рим",
        "continent": "Европа",
        "population": 60360000,
        "area": 301340,
        "fact": "В Италии находится самое маленькое государство в мире - Ватикан",
        "img_url": "https://avatars.mds.yandex.net/i?id=93b784647ff81c2cbe0036647d4eaec11d351edd-12926369-images-thumbs&n=13"
    },
    "5": {
        "name": "США",
        "capital": "Вашингтон",
        "continent": "Северная Америка",
        "population": 331000000,
        "area": 9833517,
        "fact": "Аляска была продана России США всего за 7.2 миллиона долларов в 1867 году",
        "img_url": "https://avatars.mds.yandex.net/i?id=aff8534416a86b76c4095b013a3ffce0a6d0125c-8129183-images-thumbs&n=13"
    },
    "6": {
        "name": "Китай",
        "capital": "Пекин",
        "continent": "Азия",
        "population": 1402000000,
        "area": 9596961,
        "fact": "В Китае самый большой в мире спрос на специалистов по уходу за пандами",
        "img_url": "https://avatars.mds.yandex.net/i?id=6e5a4d87dab9bac87ba81985b5eb3847bee1e2aa-5269051-images-thumbs&n=13"
    },
    "7": {
        "name": "Индия",
        "capital": "Нью-Дели",
        "continent": "Азия",
        "population": 1380000000,
        "area": 3287263,
        "fact": "В Индии есть единственное в мире плавающее почтовое отделение на озере Дал",
        "img_url": "https://avatars.mds.yandex.net/i?id=9cef4c6b82788443be73bc60f57fd960d5392e20-4078132-images-thumbs&n=13"
    },
    "8": {
        "name": "Бразилия",
        "capital": "Бразилиа",
        "continent": "Южная Америка",
        "population": 213000000,
        "area": 8515767,
        "fact": "В Бразилии находится самый большой тропический лес в мире - Амазония",
        "img_url": "https://avatars.mds.yandex.net/i?id=8039ce2e90f40380dc077732de6f20a53758dcfb-16491903-images-thumbs&n=13"
    },
    "9": {
        "name": "Австралия",
        "capital": "Канберра",
        "continent": "Австралия",
        "population": 25700000,
        "area": 7692024,
        "fact": "В Австралии живёт в 3 раза больше овец, чем людей",
        "img_url": "https://avatars.mds.yandex.net/i?id=3ea23dba71fc86499b6102df276e756a92df60a0-4707222-images-thumbs&n=13"
    },
    "10": {
        "name": "Япония",
        "capital": "Токио",
        "continent": "Азия",
        "population": 125800000,
        "area": 377975,
        "fact": "В Японии есть остров, где живут только кролики",
        "img_url": "https://avatars.mds.yandex.net/i?id=0a776b817c7817312a4a416007c342c7fa767497-9056011-images-thumbs&n=13"
    }
}

# База данных городов
cities = {
    "1": {
        "name": "Москва",
        "country": "Россия",
        "population": 13000000,
        "founded": 1147,
        "fact": "Московский Кремль - самая большая средневековая крепость в Европе",
        "img_url": "https://avatars.mds.yandex.net/i?id=ea80b565999ace59a7d72fa70411025faa5af05c-7553437-images-thumbs&n=13"
    },
    "2": {
        "name": "Париж",
        "country": "Франция",
        "population": 2161000,
        "founded": 259,
        "fact": "Эйфелеву башню перекрашивают каждые 7 лет, используя 60 тонн краски",
        "img_url": "https://avatars.mds.yandex.net/i?id=448153d6d43af75f1dafd0e52c6b754874bebdc4-10831694-images-thumbs&n=13"
    },
    "3": {
        "name": "Каир",
        "country": "Египет",
        "population": 20000000,
        "founded": 969,
        "fact": "Каир называют 'городом тысячи минаретов' из-за множества мечетей",
        "img_url": "https://avatars.mds.yandex.net/i?id=d35e042929163dd09fbc2cfe2b8a7098649e314d-8325116-images-thumbs&n=13"
    },
    "4": {
        "name": "Рим",
        "country": "Италия",
        "population": 2873000,
        "founded": 753,
        "fact": "В Риме более 900 церквей и внутри города находится целое государство - Ватикан",
        "img_url": "https://avatars.mds.yandex.net/i?id=f4d5e7d2603df773b31a74fa92df757855238fc8-17391837-images-thumbs&n=13"
    },
    "5": {
        "name": "Нью-Йорк",
        "country": "США",
        "population": 8419000,
        "founded": 1624,
        "fact": "Первоначально Нью-Йорк назывался Новый Амстердам",
        "img_url": "https://avatars.mds.yandex.net/i?id=2035d657c5ed2ce0431f0b3acdf16fc4e8337aee-12508201-images-thumbs&n=13"
    },
    "6": {
        "name": "Пекин",
        "country": "Китай",
        "population": 21540000,
        "founded": 1045,
        "fact": "Запретный город в Пекине имеет 980 зданий и 9999 комнат",
        "img_url": "https://avatars.mds.yandex.net/i?id=aeb1d7ca891b6e457c6ef3fa745ea5feaab039cc-12478411-images-thumbs&n=13"
    },
    "7": {
        "name": "Агра",
        "country": "Индия",
        "population": 1585700,
        "founded": 1504,
        "fact": "В городе Агра находится знаменитый Тадж-Махал, который меняет цвет в течение дня",
        "img_url": "https://avatars.mds.yandex.net/get-altay/14540779/2a0000019653fb09d756a15290a376253cc8/orig"
    },
    "8": {
        "name": "Рио-де-Жанейро",
        "country": "Бразилия",
        "population": 6748000,
        "founded": 1565,
        "fact": "Статуя Христа-Искупителя в Рио была выбрана одним из новых семи чудес света",
        "img_url": "https://resize.tripster.ru/WWwBite5GXIyJPls23JOUjgCY-s=/fit-in/1080x1440/filters:no_upscale()/https://cdn.tripster.ru/photos/ae30d47d-e13d-4ba6-883f-88d5b7edd21e.jpg"
    },
    "9": {
        "name": "Сидней",
        "country": "Австралия",
        "population": 5312000,
        "founded": 1788,
        "fact": "Сиднейский оперный театр имеет более 1 миллиона плиток на крыше",
        "img_url": "https://avatars.mds.yandex.net/i?id=0c161d6ce08540af0af3d5585c98780acb62776e-5268868-images-thumbs&n=13"
    },
    "10": {
        "name": "Токио",
        "country": "Япония",
        "population": 14000000,
        "founded": 1603,
        "fact": "Токийское метро - самое загруженное метро в мире",
        "img_url": "https://img.freepik.com/premium-photo/japan-crowd-city_1048944-27860930.jpg?semt=ais_hybrid&w=740"
    }
}

# База данных достопримечательностей
landmarks = {
    "1": {
        "name": "Московский Кремль",
        "city": "Москва",
        "country": "Россия",
        "type": "Крепость",
        "year": 1482,
        "fact": "Кремль имеет 20 башен, самая известная - Спасская башня с курантами",
        "img_url": "https://avatars.mds.yandex.net/i?id=e04b4d45950dbfc852fc4f9ae5bd62ede4cfb3bf-7011736-images-thumbs&n=13"
    },
    "2": {
        "name": "Эйфелева башня",
        "city": "Париж",
        "country": "Франция",
        "type": "Башня",
        "year": 1889,
        "fact": "Первоначально парижане хотели снести башню через 20 лет после постройки",
        "img_url": "https://avatars.mds.yandex.net/i?id=3838b4297c4074907d62b6d01fe59c71a721b5de-2941046-images-thumbs&n=13"
    },
    "3": {
        "name": "Пирамиды Гизы",
        "city": "Каир",
        "country": "Египет",
        "type": "Древний памятник",
        "year": -2560,
        "fact": "Великая пирамида была самым высоким сооружением в мире 3800 лет",
        "img_url": "https://resize.tripster.ru/Iw18_B2UeOs4kyCIzrF8bDCUfd8=/fit-in/1080x810/filters:no_upscale()/https://cdn.tripster.ru/photos/c918a816-e5aa-44e0-a73c-b5dfac6b8ae2.jpg"
    },
    "4": {
        "name": "Колизей",
        "city": "Рим",
        "country": "Италия",
        "type": "Амфитеатр",
        "year": 80,
        "fact": "Колизей вмещал до 50000 зрителей и имел 80 входов",
        "img_url": "https://avatars.mds.yandex.net/i?id=314d3b8caf8b48d8645ce27adc45bfc196e53e69-4055578-images-thumbs&n=13"
    },
    "5": {
        "name": "Статуя Свободы",
        "city": "Нью-Йорк",
        "country": "США",
        "type": "Памятник",
        "year": 1886,
        "fact": "Статуя Свободы была подарком Франции и везлась в США в 350 частях",
        "img_url": "https://avatars.mds.yandex.net/i?id=b9b1391727ea3317cc47a98fc7aee1bca9893002-9881038-images-thumbs&n=13"
    },
    "6": {
        "name": "Великая Китайская стена",
        "city": "Пекин",
        "country": "Китай",
        "type": "Стена",
        "year": -700,
        "fact": "Стена длиной более 21000 км, её строили более 2000 лет",
        "img_url": "https://avatars.mds.yandex.net/i?id=ac63de90484dc2306dab1ecb684e364d245eacc9-11270328-images-thumbs&n=13"
    },
    "7": {
        "name": "Тадж-Махал",
        "city": "Агра",
        "country": "Индия",
        "type": "Мавзолей",
        "year": 1653,
        "fact": "Тадж-Махал меняет цвет в зависимости от времени суток",
        "img_url": "https://avatars.mds.yandex.net/i?id=5b6f53c3a067a99593c19c85c4721d2cc06fee2f-5357859-images-thumbs&n=13"
    },
    "8": {
        "name": "Статуя Христа-Искупителя",
        "city": "Рио-де-Жанейро",
        "country": "Бразилия",
        "type": "Памятник",
        "year": 1931,
        "fact": "Статуя высотой 30 метров, размах рук - 28 метров",
        "img_url": "https://avatars.mds.yandex.net/i?id=bbc14d4c3e0714ba434355d322f1cb7bf53ab6bb-5750905-images-thumbs&n=13"
    },
    "9": {
        "name": "Сиднейский оперный театр",
        "city": "Сидней",
        "country": "Австралия",
        "type": "Театр",
        "year": 1973,
        "fact": "Крыша театра напоминает паруса и весит более 160 тонн",
        "img_url": "https://avatars.mds.yandex.net/i?id=505b285718f334ea439b55d23559c6f37623fa7b-5869999-images-thumbs&n=13"
    },
    "10": {
        "name": "Токийская башня",
        "city": "Токио",
        "country": "Япония",
        "type": "Башня",
        "year": 1958,
        "fact": "Башня покрашена в оранжевый и белый цвета для безопасности самолётов",
        "img_url": "https://avatars.mds.yandex.net/i?id=47495fa0f9733b69c0d9998739e2e1d155947c06-12431474-images-thumbs&n=13"
    },
    "11": {
        "name": "Собор Парижской Богоматери",
        "city": "Париж",
        "country": "Франция",
        "type": "Собор",
        "year": 1345,
        "fact": "Строительство собора длилось почти 200 лет",
        "img_url": "https://avatars.mds.yandex.net/i?id=eb232786ffc6ba8bc0fa8a6463c7d9844350f97e-12571073-images-thumbs&n=13"
    },
    "12": {
        "name": "Красная площадь",
        "city": "Москва",
        "country": "Россия",
        "type": "Площадь",
        "year": 1493,
        "fact": "Название 'Красная' раньше означало 'Красивая'",
        "img_url": "https://avatars.mds.yandex.net/i?id=87e6906a3ed9621543d9b118f53f705d_l-5850174-images-thumbs&n=13"
    }
}

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
        raise HTTPException(status_code=404, detail=f"Страны на континенте '{continent}' не найдены")
    logger.info(f"Запрос стран континента: {continent}")
    return result

# ========== ЭНДПОИНТЫ ДЛЯ ГОРОДОВ ==========

@cities_router.get("/all_cities")
async def get_all_cities():
    """Возвращает все города"""
    logger.info("Запрос всех городов")
    return cities

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
        raise HTTPException(status_code=404, detail=f"Достопримечательности в городе '{city}' не найдены")
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
        raise HTTPException(status_code=404, detail=f"Достопримечательности в стране '{country}' не найдены")
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
        raise HTTPException(status_code=404, detail=f"Достопримечательности типа '{type}' не найдены")
    logger.info(f"Запрос достопримечательностей типа: {type}")
    return result

# ========== ПОИСК И СТАТИСТИКА ==========

@cities_router.get("/search")
async def search_cities(query: str):
    """Поиск по всем категориям"""
    result = {
        "countries": {},
        "cities": {},
        "landmarks": {}
    }
    
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
        if (query.lower() in landmark["name"].lower() or 
            query.lower() in landmark["city"].lower() or
            query.lower() in landmark["country"].lower()):
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
        "landmark_types": {}
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