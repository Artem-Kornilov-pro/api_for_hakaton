# API для Хакатона в Школе Цифровых Технологий 🚀

Добро пожаловать в API, созданное специально для участников хакатона! Здесь собраны данные по разным темам, чтобы вы могли создавать своих Telegram-ботов и Qt-приложения, не заботясь о сложностях серверной части.

## 📚 О проекте

Этот проект предоставляет простой и понятный интерфейс для получения случайных фактов, информации о правителях, рецептов, фильмов, городов и многого другого. API создано с упором на простоту, чтобы участники хакатона могли легко в него встроиться и сосредоточиться на логике своих приложений.

**Цель проекта:** Предоставить участникам хакатона готовую, документированную базу данных с эндпоинтами разной сложности — от простых (получить случайный факт) до более продвинутых (поиск с фильтрацией).

## 🧱 Блоки данных (Категории API)

API разделено на несколько логических блоков. Каждый блок имеет свой базовый URL.

### 1. Исторические факты (`/api/historic`)
Интересные события из истории России и мира, а также информация о правителях.
*   `/facts` — все исторические факты
*   `/titles_of_facts` — названия всех исторических фактов
*   `/random_fact` — случайный исторический факт
*   `/facts/{id}` — факт по ID
*   `/facts/year/{year}` — факты за конкретный год
*   `/rulers` — все правители
*   `/names_of_rulers` — имена всех правителей
*   `/random_ruler` — случайный правитель
*   `/rulers/{id}` — правитель по ID
*   `/rulers/dynasty/{dynasty}` — правители династии (Рюриковичи, Романовы...)
*   `/stats` — статистика по базе

### 2. Кулинария (`/api/cooking`)
Шеф-повара и блюда со всего мира (русская, итальянская, французская, мексиканская, тайская, греческая и грузинская кухни).
*   `/all_chef` — все шеф-повара
*   `/names_of_all_chefs` — имена всех шеф-поваров
*   `/random_chef` — случайный шеф-повар
*   `/chef/{id}` — повар по ID
*   `/chef/born_after/{year}` — повара, родившиеся после года
*   `/chef/by_restaurant/{restaurant}` — повара ресторана
*   `/all_dishes` — все блюда
*   `/names_of_all_dishes` — названия всех блюд
*   `/random_dish` — случайное блюдо
*   `/dish/{id}` — блюдо по ID
*   `/dishes/by_country/{country}` — блюда страны
*   `/dishes/by_type/{type}` — блюда по типу (суп, салат, десерт...)
*   `/dishes/calories?min_calories=&max_calories=` — блюда в диапазоне калорий
*   `/dishes/quick?max_minutes=30` — быстрые блюда
*   `/food_info` — справочник стран и типов блюд

### 3. Кино (`/api/movies`)
Советская и современная российская классика кино.
*   `/all_movies` — все фильмы
*   `/titles_of_all_movies` — названия всех фильмов
*   `/random_movie` — случайный фильм
*   `/movie/{id}` — фильм по ID
*   `/movies_by_year/{year}` — фильмы по году
*   `/movies_by_genre/{genre}` — фильмы по жанру
*   `/top_movies` — фильмы с высоким рейтингом
*   `/all_directors` — все режиссёры
*   `/names_of_all_directors` — имена всех режиссёров
*   `/random_director` — случайный режиссёр
*   `/director/{id}` — режиссёр по ID
*   `/director_by_name/{name}` — поиск режиссёра по имени
*   `/all_actors` — все актёры
*   `/names_of_all_actors` — имена всех актёров
*   `/random_actor` — случайный актёр
*   `/actor/{id}` — актёр по ID
*   `/actor_by_name/{name}` — поиск актёра по имени
*   `/search?query=` — поиск по фильмам, режиссёрам и актёрам
*   `/movies_stats` — статистика по базе

### 4. Города и достопримечательности (`/api/cities`)
Города мира, их история и главные достопримечательности.
*   `/all_countries` — все страны
*   `/names_of_all_countries` — названия всех стран
*   `/random_country` — случайная страна
*   `/country/{id}` — страна по ID
*   `/country_by_name/{name}` — страна по названию
*   `/countries_by_continent/{continent}` — страны континента
*   `/all_cities` — все города
*   `/names_of_all_cities` — названия всех городов
*   `/random_city` — случайный город
*   `/city/{id}` — город по ID
*   `/city_by_name/{name}` — город по названию
*   `/cities_by_country/{country}` — города страны
*   `/all_landmarks` — все достопримечательности
*   `/names_of_all_landmarks` — названия всех достопримечательностей
*   `/random_landmark` — случайная достопримечательность
*   `/landmark/{id}` — достопримечательность по ID
*   `/landmarks_by_city/{city}` — достопримечательности города
*   `/landmarks_by_country/{country}` — достопримечательности страны
*   `/landmarks_by_type/{type}` — достопримечательности по типу
*   `/search?query=` — поиск по странам, городам и достопримечательностям
*   `/cities_stats` — статистика по базе

### 5. Книги и авторы (`/api/books`)
Классическая и детская литература.
*   `/all_authors` — все авторы
*   `/names_of_all_authors` — имена всех авторов
*   `/random_author` — случайный автор
*   `/author/{id}` — автор по ID
*   `/author_by_name/{name}` — поиск автора по имени
*   `/authors_by_country/{country}` — авторы страны
*   `/authors_by_genre/{genre}` — авторы жанра
*   `/all_books` — все книги
*   `/titles_of_all_books` — названия всех книг
*   `/random_book` — случайная книга
*   `/book/{id}` — книга по ID
*   `/book_by_title/{title}` — поиск книги по названию
*   `/books_by_author/{author}` — книги автора
*   `/books_by_genre/{genre}` — книги по жанру
*   `/books_by_year/{year}` — книги года
*   `/short_books?max_pages=150` — короткие книги
*   `/search_books?query=` — поиск по книгам и авторам
*   `/books_stats` — статистика по базе

## 🛠 Запуск проекта (для организаторов)

Для запуска API на сервере вам понадобятся **Docker** и **Docker Compose**. Инструкция подходит для Linux-сервера (Ubuntu/Debian).

### 1. Клонирование репозитория
```bash
git clone https://github.com/Artem-Kornilov-pro/api_for_hakaton.git
cd api_for_hakaton
```

### 2. Запуск контейнеров
```bash
docker compose up --build -d   # или: make docker-up
```

### 3. Проверка
*   `http://<адрес-сервера>:8085/ping` — должно вернуть `"PONG!"`
*   `http://<адрес-сервера>:8085/docs` — интерактивная документация со всеми эндпоинтами

### Без Docker
```bash
make install   # создаст .venv и поставит зависимости (нужен Python 3.14)
make run       # запустит API на порту 8085
```

## 👩‍💻 Для участников

```python
import requests

API = "http://<адрес-сервера>:8085"
movie = requests.get(f"{API}/api/movies/random_movie").json()
print(movie["title"], movie["year"])
```

Готовые стартовые шаблоны Telegram-бота и Qt-приложения — в папке [`examples/`](examples/).
Материалы для преподавателя — в папке [`docs/`](docs/): конспект и план хакатона.
Презентация для открытия хакатона — [`presentation/presentation_hackathon.pdf`](presentation/presentation_hackathon.pdf).