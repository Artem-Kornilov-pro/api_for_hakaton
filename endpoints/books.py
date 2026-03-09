from fastapi import APIRouter, HTTPException
import logging
import random

# Настройка логирования
logger = logging.getLogger(__name__)

books_router = APIRouter(tags=["books"])

# База данных авторов
authors = {
    "1": {
        "name": "Александр Сергеевич Пушкин",
        "birth_year": 1799,
        "death_year": 1837,
        "country": "Россия",
        "genre": "Поэзия, проза",
        "famous_works": ["Евгений Онегин", "Руслан и Людмила", "Капитанская дочка"],
        "bio": "Великий русский поэт, драматург и прозаик. Создатель современного русского литературного языка.",
        "img_url": "https://avatars.mds.yandex.net/i?id=acf4d0e235c73846b73161fa85c87e5b_l-10756139-images-thumbs&n=13"
    },
    "2": {
        "name": "Лев Николаевич Толстой",
        "birth_year": 1828,
        "death_year": 1910,
        "country": "Россия",
        "genre": "Проза",
        "famous_works": ["Война и мир", "Анна Каренина", "Детство"],
        "bio": "Один из самых известных писателей и мыслителей в мире. Его романы считаются шедеврами мировой литературы.",
        "img_url": "https://www.rusbibliophile.ru/netcat_files/multifile/1748/6923/Tolstoy_portret_3.jpg"
    },
    "3": {
        "name": "Астрид Линдгрен",
        "birth_year": 1907,
        "death_year": 2002,
        "country": "Швеция",
        "genre": "Детская литература",
        "famous_works": ["Малыш и Карлсон", "Пеппи Длинныйчулок", "Эмиль из Лённеберги"],
        "bio": "Шведская писательница, автор всемирно известных книг для детей. Её произведения переведены на 100 языков.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2265709/1238008229/S600xU_2x"
    },
    "4": {
        "name": "Джоан Роулинг",
        "birth_year": 1965,
        "country": "Великобритания",
        "genre": "Фэнтези",
        "famous_works": ["Гарри Поттер и философский камень", "Гарри Поттер и тайная комната", "Гарри Поттер и узник Азкабана"],
        "bio": "Британская писательница, создательница серии романов о Гарри Поттере. Книги переведены на 80 языков.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/10349888/1237572513/S600xU_2x"
    },
    "5": {
        "name": "Николай Носов",
        "birth_year": 1908,
        "death_year": 1976,
        "country": "Россия",
        "genre": "Детская литература",
        "famous_works": ["Приключения Незнайки", "Витя Малеев в школе и дома", "Фантазёры"],
        "bio": "Советский детский писатель. Его книги о Незнайке любимы многими поколениями детей.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2005770/1244118082/SUx182_2x"
    },
    "6": {
        "name": "Ганс Христиан Андерсен",
        "birth_year": 1805,
        "death_year": 1875,
        "country": "Дания",
        "genre": "Сказки",
        "famous_works": ["Снежная королева", "Дюймовочка", "Русалочка"],
        "bio": "Датский писатель, автор всемирно известных сказок. Его произведения переведены на 125 языков.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2057552/1228811324/SUx182_2x"
    },
    "7": {
        "name": "Эдуард Успенский",
        "birth_year": 1937,
        "death_year": 2018,
        "country": "Россия",
        "genre": "Детская литература",
        "famous_works": ["Крокодил Гена и его друзья", "Дядя Фёдор, пёс и кот", "Каникулы в Простоквашино"],
        "bio": "Советский и российский детский писатель. Создал Чебурашку, кота Матроскина и других любимых персонажей.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1727502/1246875400/SUx182_2x"
    },
    "8": {
        "name": "Александр Дюма",
        "birth_year": 1802,
        "death_year": 1870,
        "country": "Франция",
        "genre": "Приключения",
        "famous_works": ["Три мушкетёра", "Граф Монте-Кристо", "Королева Марго"],
        "bio": "Французский писатель, автор приключенческих романов. Его книги переведены на множество языков.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/10640679/1212332790/SUx182_2x"
    },
    "9": {
        "name": "Марк Твен",
        "birth_year": 1835,
        "death_year": 1910,
        "country": "США",
        "genre": "Приключения",
        "famous_works": ["Приключения Тома Сойера", "Приключения Гекльберри Финна", "Принц и нищий"],
        "bio": "Американский писатель, журналист и общественный деятель. Его книги о Томе Сойере знают во всём мире.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/10919903/1244127350/SUx182_2x"
    },
    "10": {
        "name": "Самуил Маршак",
        "birth_year": 1887,
        "death_year": 1964,
        "country": "Россия",
        "genre": "Поэзия, переводы",
        "famous_works": ["Кошкин дом", "Двенадцать месяцев", "Багаж"],
        "bio": "Русский поэт, переводчик, драматург. Его стихи знает каждый ребёнок в нашей стране.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2327175/1010035383/SUx182_2x"
    }
}

# База данных книг
books = {
    "1": {
        "title": "Евгений Онегин",
        "author": "Александр Сергеевич Пушкин",
        "year": 1833,
        "genre": "Роман в стихах",
        "pages": 224,
        "description": "Роман о трагической любви и судьбе молодого дворянина. Книга, которую называют 'энциклопедией русской жизни'.",
        "main_characters": ["Евгений Онегин", "Татьяна Ларина", "Владимир Ленский"],
        "img_url": "https://avatars.mds.yandex.net/i?id=21ad9bc87b05936cbe7ea38ed85ca7fc48ba858e-12626686-images-thumbs&n=13"
    },
    "2": {
        "title": "Война и мир",
        "author": "Лев Николаевич Толстой",
        "year": 1869,
        "genre": "Роман-эпопея",
        "pages": 1300,
        "description": "Огромное произведение о жизни русского общества в эпоху наполеоновских войн. Одна из самых длинных книг в мире.",
        "main_characters": ["Пьер Безухов", "Андрей Болконский", "Наташа Ростова"],
        "img_url": "https://avatars.mds.yandex.net/i?id=3dac0fcf4f0fb2e1f2cb5334b40f027d6b4dcaa7-5348499-images-thumbs&n=13"
    },
    "3": {
        "title": "Малыш и Карлсон",
        "author": "Астрид Линдгрен",
        "year": 1955,
        "genre": "Детская повесть",
        "pages": 128,
        "description": "Весёлая история о дружбе мальчика Малыша и Карлсона - мужчины в самом расцвете сил с пропеллером на спине.",
        "main_characters": ["Малыш", "Карлсон", "Фрекен Бок"],
        "img_url": "https://avatars.mds.yandex.net/get-mpic/16574462/2a000001993840f5f97acec182726fd714f6/orig"
    },
    "4": {
        "title": "Гарри Поттер и философский камень",
        "author": "Джоан Роулинг",
        "year": 1997,
        "genre": "Фэнтези",
        "pages": 320,
        "description": "Первая книга о мальчике, который выжил. Гарри узнаёт, что он волшебник, и поступает в Хогвартс.",
        "main_characters": ["Гарри Поттер", "Рон Уизли", "Гермиона Грейнджер"],
        "img_url": "https://avatars.mds.yandex.net/get-mpic/5283728/2a00000193570525a97541f6f8d68158b683/orig"
    },
    "5": {
        "title": "Приключения Незнайки",
        "author": "Николай Носов",
        "year": 1954,
        "genre": "Детская сказка",
        "pages": 160,
        "description": "История о малышах из Цветочного города. Незнайка постоянно попадает в забавные приключения.",
        "main_characters": ["Незнайка", "Знайка", "Пилюлькин"],
        "img_url": "https://avatars.mds.yandex.net/i?id=2810f6759d91fbcf188c0ec256883639e30e568a-4566567-images-thumbs&n=13"
    },
    "6": {
        "title": "Снежная королева",
        "author": "Ганс Христиан Андерсен",
        "year": 1844,
        "genre": "Сказка",
        "pages": 64,
        "description": "Сказка о девочке Герде, которая отправилась спасать своего друга Кая из плена Снежной королевы.",
        "main_characters": ["Герда", "Кай", "Снежная королева"],
        "img_url": "https://avatars.mds.yandex.net/i?id=6764e570d57f4ad7a6ed698533954667ec20e2c2-8220238-images-thumbs&n=13"
    },
    "7": {
        "title": "Крокодил Гена и его друзья",
        "author": "Эдуард Успенский",
        "year": 1966,
        "genre": "Детская повесть",
        "pages": 128,
        "description": "История о том, как крокодил Гена и Чебурашка строили Дом дружбы и помогали другим найти друзей.",
        "main_characters": ["Чебурашка", "Крокодил Гена", "Шапокляк"],
        "img_url": "https://avatars.mds.yandex.net/i?id=8cc44a5594d1ad16ed13b0ea5e5d2898742b1c2a-5485004-images-thumbs&n=13"
    },
    "8": {
        "title": "Три мушкетёра",
        "author": "Александр Дюма",
        "year": 1844,
        "genre": "Приключения",
        "pages": 640,
        "description": "Роман о друзьях-мушкетёрах, которые сражаются за честь королевы Франции. Девиз: 'Один за всех и все за одного!'",
        "main_characters": ["Д'Артаньян", "Атос", "Портос", "Арамис"],
        "img_url": "https://avatars.mds.yandex.net/get-mpic/1602935/2a0000019205378895dc2431e8771848560d/orig"
    },
    "9": {
        "title": "Приключения Тома Сойера",
        "author": "Марк Твен",
        "year": 1876,
        "genre": "Приключения",
        "pages": 288,
        "description": "Книга о проделках мальчика Тома, который постоянно ищет приключения и находит их.",
        "main_characters": ["Том Сойер", "Гекльберри Финн", "Бекки Тэтчер"],
        "img_url": "https://avatars.mds.yandex.net/i?id=5fdb85d63f29adde6283564b7aa833d99b220f89-8497538-images-thumbs&n=13"
    },
    "10": {
        "title": "Двенадцать месяцев",
        "author": "Самуил Маршак",
        "year": 1943,
        "genre": "Сказка",
        "pages": 96,
        "description": "Сказка о девочке, которая зимой пошла в лес за подснежниками и встретила все 12 месяцев сразу.",
        "main_characters": ["Падчерица", "Королева", "Братья-месяцы"],
        "img_url": "https://avatars.mds.yandex.net/i?id=27593f13377e88d4470226c8a865d5c72301b91a-10651281-images-thumbs&n=13"
    },
    "11": {
        "title": "Капитанская дочка",
        "author": "Александр Сергеевич Пушкин",
        "year": 1836,
        "genre": "Исторический роман",
        "pages": 224,
        "description": "История о любви и чести во время восстания Пугачёва. Книга о том, что честь нужно беречь смолоду.",
        "main_characters": ["Пётр Гринёв", "Маша Миронова", "Пугачёв"],
        "img_url": "https://avatars.mds.yandex.net/i?id=03640c5d909b4b6e6f28bd7c842cb257b29b501a-4012690-images-thumbs&n=13"
    },
    "12": {
        "title": "Дядя Фёдор, пёс и кот",
        "author": "Эдуард Успенский",
        "year": 1974,
        "genre": "Детская повесть",
        "pages": 160,
        "description": "История о мальчике, который уехал жить в деревню с котом Матроскиным и псом Шариком.",
        "main_characters": ["Дядя Фёдор", "Кот Матроскин", "Пёс Шарик", "Печкин"],
        "img_url": "https://avatars.mds.yandex.net/i?id=2ab969e418f5d08c18be275667348fc773bafc99-12630334-images-thumbs&n=13"
    }
}

# Вспомогательная функция
def get_item_or_404(data_dict, item_id, item_name):
    if item_id not in data_dict:
        raise HTTPException(status_code=404, detail=f"{item_name} с ID {item_id} не найден")
    return data_dict[item_id]

# ========== ЭНДПОИНТЫ ДЛЯ АВТОРОВ ==========

@books_router.get("/all_authors")
async def get_all_authors():
    """Возвращает всех авторов"""
    logger.info("Запрос всех авторов")
    return authors

@books_router.get("/random_author")
async def get_random_author():
    """Возвращает случайного автора"""
    author_id = random.choice(list(authors.keys()))
    logger.info(f"Случайный автор с ID: {author_id}")
    return authors[author_id]

@books_router.get("/author/{author_id}")
async def get_author_by_id(author_id: str):
    """Возвращает автора по ID"""
    return get_item_or_404(authors, author_id, "Автор")

@books_router.get("/author_by_name/{name}")
async def get_author_by_name(name: str):
    """Поиск автора по имени"""
    for id, author in authors.items():
        if name.lower() in author["name"].lower():
            logger.info(f"Найден автор: {author['name']}")
            return author
    raise HTTPException(status_code=404, detail=f"Автор '{name}' не найден")

@books_router.get("/authors_by_country/{country}")
async def get_authors_by_country(country: str):
    """Возвращает авторов из указанной страны"""
    result = {}
    for id, author in authors.items():
        if country.lower() in author["country"].lower():
            result[id] = author
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Авторы из страны '{country}' не найдены")
    logger.info(f"Запрос авторов из страны: {country}")
    return result

@books_router.get("/authors_by_genre/{genre}")
async def get_authors_by_genre(genre: str):
    """Возвращает авторов, пишущих в указанном жанре"""
    result = {}
    for id, author in authors.items():
        if genre.lower() in author["genre"].lower():
            result[id] = author
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Авторы в жанре '{genre}' не найдены")
    logger.info(f"Запрос авторов в жанре: {genre}")
    return result

# ========== ЭНДПОИНТЫ ДЛЯ КНИГ ==========

@books_router.get("/all_books")
async def get_all_books():
    """Возвращает все книги"""
    logger.info("Запрос всех книг")
    return books

@books_router.get("/random_book")
async def get_random_book():
    """Возвращает случайную книгу"""
    book_id = random.choice(list(books.keys()))
    logger.info(f"Случайная книга с ID: {book_id}")
    return books[book_id]

@books_router.get("/book/{book_id}")
async def get_book_by_id(book_id: str):
    """Возвращает книгу по ID"""
    return get_item_or_404(books, book_id, "Книга")

@books_router.get("/book_by_title/{title}")
async def get_book_by_title(title: str):
    """Поиск книги по названию"""
    for id, book in books.items():
        if title.lower() in book["title"].lower():
            logger.info(f"Найдена книга: {book['title']}")
            return book
    raise HTTPException(status_code=404, detail=f"Книга '{title}' не найдена")

@books_router.get("/books_by_author/{author}")
async def get_books_by_author(author: str):
    """Возвращает книги указанного автора"""
    result = {}
    for id, book in books.items():
        if author.lower() in book["author"].lower():
            result[id] = book
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Книги автора '{author}' не найдены")
    logger.info(f"Запрос книг автора: {author}")
    return result

@books_router.get("/books_by_genre/{genre}")
async def get_books_by_genre(genre: str):
    """Возвращает книги указанного жанра"""
    result = {}
    for id, book in books.items():
        if genre.lower() in book["genre"].lower():
            result[id] = book
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Книги в жанре '{genre}' не найдены")
    logger.info(f"Запрос книг в жанре: {genre}")
    return result

@books_router.get("/books_by_year/{year}")
async def get_books_by_year(year: int):
    """Возвращает книги, опубликованные в указанном году"""
    result = {}
    for id, book in books.items():
        if book["year"] == year:
            result[id] = book
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Книги {year} года не найдены")
    logger.info(f"Запрос книг {year} года")
    return result

@books_router.get("/short_books")
async def get_short_books(max_pages: int = 150):
    """Возвращает книги, в которых меньше указанного количества страниц"""
    result = {}
    for id, book in books.items():
        if book["pages"] <= max_pages:
            result[id] = book
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Книги с количеством страниц до {max_pages} не найдены")
    logger.info(f"Запрос книг до {max_pages} страниц")
    return result

# ========== ПОИСК И СТАТИСТИКА ==========

@books_router.get("/search_books")
async def search_books(query: str):
    """Поиск по книгам и авторам"""
    result = {
        "authors": {},
        "books": {}
    }
    
    # Поиск в авторах
    for id, author in authors.items():
        if (query.lower() in author["name"].lower() or 
            any(query.lower() in work.lower() for work in author["famous_works"])):
            result["authors"][id] = author
    
    # Поиск в книгах
    for id, book in books.items():
        if (query.lower() in book["title"].lower() or 
            query.lower() in book["author"].lower() or
            any(query.lower() in char.lower() for char in book["main_characters"])):
            result["books"][id] = book
    
    total = len(result["authors"]) + len(result["books"])
    if total == 0:
        raise HTTPException(status_code=404, detail=f"По запросу '{query}' ничего не найдено")
    
    logger.info(f"Поиск '{query}' дал {total} результатов")
    return result

@books_router.get("/books_stats")
async def get_books_stats():
    """Статистика по базе данных книг"""
    # Самый популярный жанр
    genres = {}
    for book in books.values():
        genre = book["genre"]
        genres[genre] = genres.get(genre, 0) + 1
    
    most_popular_genre = max(genres, key=genres.get) if genres else "Нет данных"
    
    # Самая длинная и короткая книга
    longest_book = max(books.values(), key=lambda x: x["pages"]) if books else None
    shortest_book = min(books.values(), key=lambda x: x["pages"]) if books else None
    
    stats = {
        "total_authors": len(authors),
        "total_books": len(books),
        "average_pages": sum(book["pages"] for book in books.values()) // len(books) if books else 0,
        "oldest_book": min(books.values(), key=lambda x: x["year"]) if books else None,
        "newest_book": max(books.values(), key=lambda x: x["year"]) if books else None,
        "longest_book": longest_book["title"] if longest_book else None,
        "shortest_book": shortest_book["title"] if shortest_book else None,
        "most_popular_genre": most_popular_genre,
        "genres_count": genres,
        "authors_by_country": {}
    }
    
    # Авторы по странам
    for author in authors.values():
        country = author["country"]
        stats["authors_by_country"][country] = stats["authors_by_country"].get(country, 0) + 1
    
    logger.info("Запрос статистики по книгам")
    return stats