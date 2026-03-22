from locust import HttpUser, task, between
import random
import json


class ApiHakatonUser(HttpUser):
    """
    Пользователь, который тестирует API для хакатона
    """

    wait_time = between(1, 3)  # Пауза между запросами 1-3 секунды

    def on_start(self):
        """Выполняется при старте каждого пользователя"""
        # Получаем списки ID для случайных запросов
        self.historic_ids = []
        self.cooking_ids = []
        self.movies_ids = []
        self.cities_ids = []
        self.books_ids = []

        # Загружаем данные для получения ID
        self.init_data()

    def init_data(self):
        """Инициализация данных для случайных запросов"""
        # Получаем ID исторических фактов
        with self.client.get("/api/historic/facts", catch_response=True) as response:
            if response.status_code == 200:
                facts = response.json()
                self.historic_ids = list(facts.keys())

        # Получаем ID правителей
        with self.client.get("/api/historic/rulers", catch_response=True) as response:
            if response.status_code == 200:
                rulers = response.json()
                self.rulers_ids = list(rulers.keys())

        # Получаем ID блюд
        with self.client.get("/api/cooking/all_dishes", catch_response=True) as response:
            if response.status_code == 200:
                dishes = response.json()
                self.dishes_ids = list(dishes.keys())

        # Получаем ID поваров
        with self.client.get("/api/cooking/all_chef", catch_response=True) as response:
            if response.status_code == 200:
                chefs = response.json()
                self.chefs_ids = list(chefs.keys())

        # Получаем ID фильмов
        with self.client.get("/api/movies/all_movies", catch_response=True) as response:
            if response.status_code == 200:
                movies = response.json()
                self.movies_ids = list(movies.keys())

        # Получаем ID городов
        with self.client.get("/api/cities/all_cities", catch_response=True) as response:
            if response.status_code == 200:
                cities = response.json()
                self.cities_ids = list(cities.keys())

        # Получаем ID достопримечательностей
        with self.client.get("/api/cities/all_landmarks", catch_response=True) as response:
            if response.status_code == 200:
                landmarks = response.json()
                self.landmarks_ids = list(landmarks.keys())

        # Получаем ID книг
        with self.client.get("/api/books/all_books", catch_response=True) as response:
            if response.status_code == 200:
                books = response.json()
                self.books_ids = list(books.keys())

        # Получаем ID авторов
        with self.client.get("/api/books/all_authors", catch_response=True) as response:
            if response.status_code == 200:
                authors = response.json()
                self.authors_ids = list(authors.keys())

    # ========== ПРОСТЫЕ ЭНДПОИНТЫ ==========

    @task(5)
    def ping(self):
        """Проверка работоспособности"""
        self.client.get("/ping")

    @task(3)
    def get_random_fact(self):
        """Случайный исторический факт"""
        self.client.get("/api/historic/random_fact")

    @task(3)
    def get_random_ruler(self):
        """Случайный правитель"""
        self.client.get("/api/historic/random_ruler")

    @task(3)
    def get_random_dish(self):
        """Случайное блюдо"""
        self.client.get("/api/cooking/random_dish")

    @task(3)
    def get_random_chef(self):
        """Случайный повар"""
        self.client.get("/api/cooking/random_chef")

    @task(3)
    def get_random_movie(self):
        """Случайный фильм"""
        self.client.get("/api/movies/random_movie")

    @task(3)
    def get_random_city(self):
        """Случайный город"""
        self.client.get("/api/cities/random_city")

    @task(3)
    def get_random_landmark(self):
        """Случайная достопримечательность"""
        self.client.get("/api/cities/random_landmark")

    @task(3)
    def get_random_book(self):
        """Случайная книга"""
        self.client.get("/api/books/random_book")

    @task(3)
    def get_random_author(self):
        """Случайный автор"""
        self.client.get("/api/books/random_author")

    # ========== ЭНДПОИНТЫ СО ВСЕМИ ДАННЫМИ ==========

    @task(2)
    def get_all_facts(self):
        """Все исторические факты"""
        self.client.get("/api/historic/facts")

    @task(2)
    def get_all_rulers(self):
        """Все правители"""
        self.client.get("/api/historic/rulers")

    @task(2)
    def get_all_dishes(self):
        """Все блюда"""
        self.client.get("/api/cooking/all_dishes")

    @task(2)
    def get_all_chefs(self):
        """Все повара"""
        self.client.get("/api/cooking/all_chef")

    @task(2)
    def get_all_movies(self):
        """Все фильмы"""
        self.client.get("/api/movies/all_movies")

    @task(2)
    def get_all_cities(self):
        """Все города"""
        self.client.get("/api/cities/all_cities")

    @task(2)
    def get_all_landmarks(self):
        """Все достопримечательности"""
        self.client.get("/api/cities/all_landmarks")

    @task(2)
    def get_all_books(self):
        """Все книги"""
        self.client.get("/api/books/all_books")

    @task(2)
    def get_all_authors(self):
        """Все авторы"""
        self.client.get("/api/books/all_authors")

    # ========== ЭНДПОИНТЫ ПО ID ==========

    @task(1)
    def get_fact_by_id(self):
        """Факт по ID"""
        if self.historic_ids:
            fact_id = random.choice(self.historic_ids)
            self.client.get(f"/api/historic/facts/{fact_id}")

    @task(1)
    def get_ruler_by_id(self):
        """Правитель по ID"""
        if hasattr(self, "rulers_ids") and self.rulers_ids:
            ruler_id = random.choice(self.rulers_ids)
            self.client.get(f"/api/historic/rulers/{ruler_id}")

    @task(1)
    def get_dish_by_id(self):
        """Блюдо по ID"""
        if hasattr(self, "dishes_ids") and self.dishes_ids:
            dish_id = random.choice(self.dishes_ids)
            self.client.get(f"/api/cooking/dish/{dish_id}")

    @task(1)
    def get_chef_by_id(self):
        """Повар по ID"""
        if hasattr(self, "chefs_ids") and self.chefs_ids:
            chef_id = random.choice(self.chefs_ids)
            self.client.get(f"/api/cooking/chef/{chef_id}")

    @task(1)
    def get_movie_by_id(self):
        """Фильм по ID"""
        if hasattr(self, "movies_ids") and self.movies_ids:
            movie_id = random.choice(self.movies_ids)
            self.client.get(f"/api/movies/movie/{movie_id}")

    @task(1)
    def get_city_by_id(self):
        """Город по ID"""
        if hasattr(self, "cities_ids") and self.cities_ids:
            city_id = random.choice(self.cities_ids)
            self.client.get(f"/api/cities/city/{city_id}")

    @task(1)
    def get_landmark_by_id(self):
        """Достопримечательность по ID"""
        if hasattr(self, "landmarks_ids") and self.landmarks_ids:
            landmark_id = random.choice(self.landmarks_ids)
            self.client.get(f"/api/cities/landmark/{landmark_id}")

    @task(1)
    def get_book_by_id(self):
        """Книга по ID"""
        if hasattr(self, "books_ids") and self.books_ids:
            book_id = random.choice(self.books_ids)
            self.client.get(f"/api/books/book/{book_id}")

    @task(1)
    def get_author_by_id(self):
        """Автор по ID"""
        if hasattr(self, "authors_ids") and self.authors_ids:
            author_id = random.choice(self.authors_ids)
            self.client.get(f"/api/books/author/{author_id}")

    # ========== ПОИСКОВЫЕ ЭНДПОИНТЫ ==========

    @task(1)
    def search_books(self):
        """Поиск книг"""
        queries = ["Пушкин", "Гарри", "война", "Толстой", "детство"]
        query = random.choice(queries)
        self.client.get(f"/api/books/search_books?query={query}")

    @task(1)
    def search_movies(self):
        """Поиск по фильмам"""
        queries = ["Гайдай", "Балабанов", "Иван", "брат", "Москва"]
        query = random.choice(queries)
        self.client.get(f"/api/movies/search?query={query}")

    @task(1)
    def search_cities(self):
        """Поиск по городам"""
        queries = ["Москва", "Россия", "Европа", "Париж", "Кремль"]
        query = random.choice(queries)
        self.client.get(f"/api/cities/search?query={query}")

    # ========== ФИЛЬТРЫ ==========

    @task(1)
    def get_movies_by_year(self):
        """Фильмы по году"""
        years = [1965, 1973, 1997, 2000, 2013]
        year = random.choice(years)
        self.client.get(f"/api/movies/movies_by_year/{year}")

    @task(1)
    def get_movies_by_genre(self):
        """Фильмы по жанру"""
        genres = ["Комедия", "Драма", "Фэнтези"]
        genre = random.choice(genres)
        self.client.get(f"/api/movies/movies_by_genre/{genre}")

    @task(1)
    def get_dishes_by_country(self):
        """Блюда по стране"""
        countries = ["Россия", "Италия", "Франция", "Греция", "Грузия"]
        country = random.choice(countries)
        self.client.get(f"/api/cooking/dishes/by_country/{country}")

    @task(1)
    def get_dishes_by_type(self):
        """Блюда по типу"""
        types = ["Суп", "Салат", "Десерт", "Основное блюдо"]
        dish_type = random.choice(types)
        self.client.get(f"/api/cooking/dishes/by_type/{dish_type}")

    @task(1)
    def get_landmarks_by_type(self):
        """Достопримечательности по типу"""
        types = ["Крепость", "Собор", "Музей", "Памятник", "Башня"]
        landmark_type = random.choice(types)
        self.client.get(f"/api/cities/landmarks_by_type/{landmark_type}")

    # ========== СТАТИСТИКА ==========

    @task(1)
    def get_stats(self):
        """Статистика"""
        endpoints = [
            "/api/historic/stats",
            "/api/cooking/food_info",
            "/api/movies/movies_stats",
            "/api/cities/cities_stats",
            "/api/books/books_stats",
        ]
        endpoint = random.choice(endpoints)
        self.client.get(endpoint)
