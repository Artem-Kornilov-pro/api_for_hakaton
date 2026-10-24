import requests
import telebot

API = "http://127.0.0.1:8085"  # адрес сервера даст преподаватель
TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BotFather"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /movie — и я посоветую фильм.")


@bot.message_handler(commands=["movie"])
def random_movie(message):
    movie = requests.get(f"{API}/api/movies/random_movie").json()
    text = f"{movie['title']} ({movie['year']})\nРейтинг: {movie['rating']}\n\n"
    text += movie["description"]
    try:
        bot.send_photo(message.chat.id, movie["img_url"], caption=text)
    except Exception:
        # Telegram не смог скачать картинку — отправим просто текст
        bot.send_message(message.chat.id, text)


if __name__ == "__main__":
    bot.infinity_polling()
