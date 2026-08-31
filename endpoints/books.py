import logging
import random
from typing import Any

from fastapi import APIRouter, HTTPException

from data.books import authors, books

# Настройка логирования
logger = logging.getLogger(__name__)

books_router = APIRouter(tags=["books"])


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

@books_router.get("/names_of_all_authors")
async def names_of_all_authors():
    """Возвращает имена всех авторов"""
    logger.info("Запрос имён всех авторов")
    return [ author["name"] for author in authors.values()]


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

@books_router.get("/titles_of_all_books")
async def get_titles_of_all_books():
    """Возвращает названия всех книги"""
    logger.info("Запрос названия всех книг")
    return [ book["title"] for book in books.values()]


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
        raise HTTPException(
            status_code=404, detail=f"Книги с количеством страниц до {max_pages} не найдены"
        )
    logger.info(f"Запрос книг до {max_pages} страниц")
    return result


# ========== ПОИСК И СТАТИСТИКА ==========


@books_router.get("/search_books")
async def search_books(query: str):
    """Поиск по книгам и авторам"""
    result: dict[str, dict[str, Any]] = {"authors": {}, "books": {}}

    # Поиск в авторах
    for id, author in authors.items():
        if query.lower() in author["name"].lower() or any(
            query.lower() in work.lower() for work in author["famous_works"]
        ):
            result["authors"][id] = author

    # Поиск в книгах
    for id, book in books.items():
        if (
            query.lower() in book["title"].lower()
            or query.lower() in book["author"].lower()
            or any(query.lower() in char.lower() for char in book["main_characters"])
        ):
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
        "average_pages": sum(book["pages"] for book in books.values()) // len(books)
        if books
        else 0,
        "oldest_book": min(books.values(), key=lambda x: x["year"]) if books else None,
        "newest_book": max(books.values(), key=lambda x: x["year"]) if books else None,
        "longest_book": longest_book["title"] if longest_book else None,
        "shortest_book": shortest_book["title"] if shortest_book else None,
        "most_popular_genre": most_popular_genre,
        "genres_count": genres,
        "authors_by_country": {},
    }

    # Авторы по странам
    for author in authors.values():
        country = author["country"]
        stats["authors_by_country"][country] = stats["authors_by_country"].get(country, 0) + 1

    logger.info("Запрос статистики по книгам")
    return stats
