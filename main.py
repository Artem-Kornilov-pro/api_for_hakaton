from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import uvicorn
from endpoints.historic import historic_router
from endpoints.cooking import cooking_router
from endpoints.movies import movies_router
from endpoints.cities import cities_router
from endpoints.books import books_router

#from endpoints.auth import auth
#from endpoints.chat import chat_router




app = FastAPI()

# Максимально открытый CORS — разрешаем всё со всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # любой сайт, любой домен, любой порт
    allow_credentials=True,        # куки, Authorization заголовки и т.д.
    allow_methods=["*"],           # GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD…
    allow_headers=["*"],           # любые заголовки, включая кастомные
    expose_headers=["*"],          # если фронту нужны твои кастомные заголовки в ответе
    max_age=86400,                 # кэшируем preflight-запрос на 24 часа
)



@app.get("/ping")
def pinger():
    return "PONG!"

# Подключаем роутеры
app.include_router(historic_router, prefix="/api/historic")
app.include_router(cooking_router, prefix="/api/cooking")
app.include_router(movies_router, prefix="/api/movies")
app.include_router(cities_router, prefix="/api/cities")
app.include_router(books_router, prefix="/api/books")


"""
if __name__ == "__main__": 
    # Запуск приложения
    uvicorn.run(app, host="0.0.0.0", port=8085)
"""
