import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

API = "http://127.0.0.1:8085"  # адрес сервера даст преподаватель
# Wikimedia не отдаёт картинки программам, которые не представились
HEADERS = {"User-Agent": "ShctHackathonApp/1.0 (school project)"}


class MovieWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Случайный фильм")
        self.picture = QLabel()
        self.text = QLabel("Нажми на кнопку")
        self.text.setWordWrap(True)
        button = QPushButton("Посоветуй фильм")
        button.clicked.connect(self.show_movie)

        layout = QVBoxLayout(self)
        layout.addWidget(self.picture)
        layout.addWidget(self.text)
        layout.addWidget(button)

    def show_movie(self):
        movie = requests.get(f"{API}/api/movies/random_movie").json()
        self.text.setText(f"{movie['title']} ({movie['year']}), рейтинг {movie['rating']}")
        self.show_picture(movie["img_url"])

    def show_picture(self, url):
        pixmap = QPixmap()
        if url:
            data = requests.get(url, headers=HEADERS, timeout=10).content
            pixmap.loadFromData(data)
        if pixmap.isNull():
            self.picture.setText("(нет картинки)")
        else:
            self.picture.setPixmap(pixmap.scaledToWidth(300))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieWindow()
    window.show()
    sys.exit(app.exec())
