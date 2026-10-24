"""
Собирает презентацию хакатона в стиле ШЦТ: presentation_hackathon.html + .pdf.

Запуск:  python3 build_slides.py                         — HTML и PDF
         python3 build_slides.py --server 192.168.1.10   — подставить адрес сервера в слайды
         python3 build_slides.py --preview               — ещё и PNG каждого слайда в preview/

Нужен только Chromium (headless). Путь берётся из переменной CHROME,
иначе — из кэша Playwright или из Google Chrome.
"""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = "presentation_hackathon"
# Адрес сервера API: в примерах кода и на последнем слайде (без --server там остаётся пропуск)
SERVER = sys.argv[sys.argv.index("--server") + 1] if "--server" in sys.argv else None
EXAMPLE_IP = SERVER or "192.168.1.10"

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    *sorted(
        Path.home().glob(
            "Library/Caches/ms-playwright/chromium_headless_shell-*/"
            "chrome-headless-shell-mac-arm64/chrome-headless-shell"
        ),
        reverse=True,
    ),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

# ---- CSS из шаблона ШЦТ (без изменений) ----
CSS = """
@page { size: 1440px 810px; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: var(--font), Arial, sans-serif; color: var(--ink); background: #fff }
.slide { width: 1440px; height: 810px; position: relative; overflow: hidden; page-break-after: always;
         background: var(--bg); padding: 0 72px }
.logo { position: absolute; left: 64px; top: 38px; height: 56px; z-index: 5 }
h1 { font-size: 92px; line-height: 1.04; font-weight: var(--hw); letter-spacing: -1px }
h2 { font-size: 58px; line-height: 1.1; font-weight: var(--hw); position: absolute; left: 72px; top: 120px; z-index: 3 }
em { font-style: normal; color: var(--accent) }
.lead { font-size: 30px; line-height: 1.4; font-weight: 600 }
.body { position: absolute; left: 72px; right: 72px; top: 215px; bottom: 50px }
.row { display: flex; gap: 28px; height: 100% }
.col { display: flex; flex-direction: column; gap: 22px }
.card { background: var(--card); border: var(--cardborder); border-radius: var(--radius); padding: 28px 30px;
        box-shadow: var(--shadow); flex: 1; position: relative }
.card h3 { font-size: 30px; font-weight: 800; margin-bottom: 10px; line-height: 1.15 }
.card p, .txt { font-size: 24px; line-height: 1.38; font-weight: 600; color: var(--text) }
.big .card p { font-size: 28px } .big .card h3 { font-size: 32px } .big .card { align-self: flex-start; min-height: 400px }
.sm p { font-size: 21px } .sm h3 { font-size: 26px; margin-bottom: 6px }
.num { width: 64px; height: 64px; border-radius: 50%; background: var(--grad); color: #fff; font-weight: 800;
       font-size: 32px; display: flex; align-items: center; justify-content: center; margin-bottom: 18px }
.img { border-radius: 24px; display: block; box-shadow: var(--shadow) }
.chip { display: inline-block; background: var(--soft); color: var(--accent); font-weight: 800; font-size: 22px;
        padding: 6px 16px; border-radius: 999px }
.cap { font-size: 22px; font-weight: 700; margin-top: 12px; text-align: center; line-height: 1.25 }
.code { background: #17142b; color: #e9e6ff; border-radius: 28px; padding: 30px 36px; font-family: 'JetBrains Mono', Menlo, monospace;
        font-size: 24px; line-height: 1.5; white-space: pre; box-shadow: var(--shadow) }
.code .c { color: #8f8ab8 } .code .k { color: #ff9ad5 } .code .s { color: #9be29b } .code .n { color: #ffd479 }
.arrow { font-size: 54px; font-weight: 800; color: var(--accent); align-self: center }
.grad { background: var(--grad); color: #fff }
.grad h2 { color: #fff } .grad em { color: #fff; text-decoration: underline; text-decoration-thickness: 6px }
.grad .card { background: #fff; color: var(--ink) }
.deco { position: absolute; z-index: 1 }
.pagenum { position: absolute; right: 40px; bottom: 22px; font-weight: 800; font-size: 20px; color: var(--accent); opacity: .8 }
.grad .pagenum { color: #fff }
.tr td { padding: 12px 18px; font-size: 24px; font-weight: 600; border-bottom: 2px solid var(--soft) }

.t-shct { --font: 'Open Sans'; --ink: #0b0b1c; --text: #33334d; --accent: #7b2ff2; --soft: #f1e8ff; --bg: #fff; --card: #fff;
  --grad: linear-gradient(135deg, #e02cf3 0%, #7b3df5 50%, #2740ee 100%); --hw: 800; --radius: 34px;
  --cardborder: 4px solid transparent; --shadow: 0 10px 30px rgba(90,40,200,.18) }
.t-shct .card { background: linear-gradient(#fff, #fff) padding-box, var(--grad) border-box }
.t-shct .grad .card { background: linear-gradient(#fff, #fff) padding-box, linear-gradient(135deg,#fff,#fff) border-box }
.t-shct .sphere { border-radius: 50%; background: linear-gradient(135deg, #e02cf3, #3a3df5) }
"""

# ---- Дополнения для слайдов хакатона ----
CSS_EXTRA = """
.mono { font-family: 'JetBrains Mono', Menlo, monospace }
.gnum { font-size: 64px; font-weight: 800; line-height: 1; color: var(--accent) }
.flowbox { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center }
.msg { font-family: 'JetBrains Mono', Menlo, monospace; font-size: 22px; font-weight: 700; background: var(--soft);
       color: var(--accent); border-radius: 16px; padding: 10px 16px; white-space: nowrap }
.url { display: flex; align-items: flex-start; justify-content: center; gap: 6px }
.url .seg { display: flex; flex-direction: column; align-items: center; gap: 14px }
.url .part { font-family: 'JetBrains Mono', Menlo, monospace; font-size: 37px; font-weight: 700; padding: 14px 18px;
             border-radius: 18px; white-space: nowrap }
.url .lbl { font-size: 22px; font-weight: 800; color: var(--text) }
.p1 { background: #fde7ff; color: #b416c8 } .p2 { background: #efe6ff; color: #7b2ff2 }
.p3 { background: #e6e9ff; color: #3446e8 } .p4 { background: #e3f6ec; color: #1f8a4c }
.tg { width: 330px; height: 545px; border-radius: 44px; border: 10px solid #15132a; overflow: hidden; position: relative;
      background: linear-gradient(160deg, #d9ecd2, #b8d8c4); box-shadow: var(--shadow); flex: none }
.tg .bar { background: #fff; padding: 16px 18px; display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 19px }
.tg .ava { width: 40px; height: 40px; border-radius: 50%; background: var(--grad); color: #fff; display: flex;
           align-items: center; justify-content: center; font-size: 18px }
.tg .bar small { display: block; font-weight: 600; font-size: 14px; color: #7a8a99 }
.tg .chat { padding: 16px 14px; display: flex; flex-direction: column; gap: 12px }
.bub { max-width: 86%; border-radius: 18px; padding: 10px 14px; font-size: 17px; line-height: 1.35; font-weight: 600;
       box-shadow: 0 1px 2px rgba(0,0,0,.12) }
.bub.me { align-self: flex-end; background: #e1fec6; font-family: 'JetBrains Mono', Menlo, monospace; color: #2a7bd6 }
.bub.bot { align-self: flex-start; background: #fff; padding: 6px; max-width: 92% }
.bub.bot img { width: 100%; border-radius: 13px; display: block }
.bub.bot div { padding: 8px 8px 4px }
.win { border-radius: 18px; overflow: hidden; box-shadow: var(--shadow); background: #ececec; flex: none;
       border: 1px solid #d4d4dc }
.win .tbar { height: 38px; display: flex; align-items: center; gap: 8px; padding: 0 14px; background: #e3e3e8;
             font-size: 16px; font-weight: 700; color: #555 }
.win .dot { width: 13px; height: 13px; border-radius: 50% }
.win img { display: block }
.hl { background: rgba(255, 212, 121, .16); border-radius: 6px; outline: 2px solid rgba(255, 212, 121, .55) }
.plus, .minus { display: flex; gap: 14px; font-size: 24px; font-weight: 600; line-height: 1.35; color: var(--text) }
.plus b, .minus b { flex: none; width: 34px; height: 34px; border-radius: 50%; color: #fff; display: flex;
                    align-items: center; justify-content: center; font-size: 24px; margin-top: 1px }
.plus b { background: var(--grad) } .minus b { background: #b9b6cc }
.stars { color: var(--accent); font-size: 24px; letter-spacing: 2px }
.ep { font-family: 'JetBrains Mono', Menlo, monospace; font-size: 16px; color: var(--accent); font-weight: 700;
      margin-top: 10px; line-height: 1.45 }
.stairs { display: flex; gap: 18px; align-items: flex-end; height: 100% }
.stairs .card { padding: 22px 20px; flex: 1 }
.stairs .num { width: 52px; height: 52px; font-size: 26px; margin-bottom: 12px }
.stairs h3 { font-size: 25px } .stairs p { font-size: 19px }
.err h3 { font-family: 'JetBrains Mono', Menlo, monospace; font-size: 23px; color: var(--accent) }
.err p { font-size: 21px }
.bars { display: flex; flex-direction: column; gap: 22px }
.bars .b { display: grid; grid-template-columns: 300px 1fr 70px; align-items: center; gap: 18px; font-size: 25px; font-weight: 700 }
.bars .track { height: 34px; border-radius: 20px; background: var(--soft) }
.bars .fill { height: 100%; border-radius: 20px; background: var(--grad) }
.bars .pts { font-size: 30px; font-weight: 800; color: var(--accent); text-align: right }
.tl { position: relative; height: 100% }
.tl .line { position: absolute; left: 0; right: 0; top: 118px; height: 8px; border-radius: 4px; background: var(--grad) }
.tl .stop { position: absolute; top: 0; width: 144px; text-align: center }
.tl .t { font-size: 25px; font-weight: 800; height: 40px }
.tl .d { width: 30px; height: 30px; border-radius: 50%; background: #fff; border: 7px solid var(--accent);
         margin: 60px auto 0 }
.tl .stop.on .d { background: var(--accent) }
.tl .w { font-size: 20px; font-weight: 700; line-height: 1.3; margin-top: 30px; color: var(--ink); padding: 0 6px }
.tl .cp { display: inline-block; margin-top: 10px; font-size: 15px; font-weight: 800; color: var(--accent);
          background: var(--soft); border-radius: 999px; padding: 4px 10px }
.addr { font-family: 'JetBrains Mono', Menlo, monospace; font-size: 38px; font-weight: 700; color: var(--accent);
        border-bottom: 4px dashed var(--accent); padding-bottom: 4px }

/* Градиентная рамка карточек без двух слоёв фона: в PDF белый слой-градиент
   печатался со щелями, сквозь которые просвечивала фиолетовая полоса */
.t-shct .card { background: var(--grad) border-box; isolation: isolate }
.t-shct .card::before { content: ""; position: absolute; inset: 0; background: #fff;
  border-radius: calc(var(--radius) - 4px); z-index: -1 }

/* В PDF размытая тень печатается жёсткими фиолетовыми плашками, которые наползают
   друг на друга, — для печати тени отключаем, на экране они остаются */
@media print {
  .t-shct { --shadow: none }
  .bub { box-shadow: none }
}
"""

LOGO = '<img class="logo" src="assets/logo_shct.png">'
SPHERE = '<div class="deco sphere" style="right:70px;top:46px;width:54px;height:54px"></div>'


def slide(title, body, n, cls=""):
    logo = '<img class="logo" src="assets/logo_shct_white.png">' if cls == "grad" else LOGO + SPHERE
    return (
        f'<section class="slide {cls}">{logo}<h2>{title}</h2>'
        f'<div class="body">{body}</div><div class="pagenum">{n}</div></section>'
    )


def s_title():
    return f"""<section class="slide">{LOGO}
    <img class="deco" src="assets/shape_crop.jpg" style="right:0;top:0;height:810px">
    <div class="deco sphere" style="left:760px;top:96px;width:96px;height:96px"></div>
    <div style="position:absolute;left:72px;top:170px;width:860px">
      <div class="chip" style="margin-bottom:28px">Хакатон по Python · 11–17 лет</div>
      <h1 style="font-size:84px">Свой бот<br>или приложение<br><em>за один день</em></h1>
      <p class="lead" style="margin-top:34px;width:760px">Данные уже лежат на сервере. Твоя задача —
      придумать программу и написать её.</p></div></section>"""


def s_plan(n):
    cards = [
        ("Узнаем", "что такое API и как программа «разговаривает» с сервером"),
        ("Выберем", "трек: Telegram-бот или приложение на Qt"),
        ("Напишем", "программу на Python с данными из API"),
        ("Покажем", "демо за 3 минуты — и награждение"),
    ]
    body = "".join(
        f'<div class="card"><div class="num">{i}</div><h3>{h}</h3><p>{p}</p></div>'
        for i, (h, p) in enumerate(cards, 1)
    )
    return slide("Что нас <em>ждёт</em>", f'<div class="row big">{body}</div>', n)


def s_api(n):
    body = """<div class="col" style="height:100%;gap:30px">
      <div class="row" style="height:auto;align-items:stretch">
        <div class="card flowbox" style="flex:none;width:330px;height:260px"><div style="font-size:70px">💻</div>
          <h3 style="margin-top:8px">Твоя программа</h3><p>бот или окно</p></div>
        <div class="col" style="flex:1;justify-content:center;gap:34px;align-items:center">
          <div class="col" style="gap:8px;align-items:center"><div class="msg">GET /api/movies/random_movie</div>
            <div class="arrow" style="font-size:44px;line-height:1">запрос →</div></div>
          <div class="col" style="gap:8px;align-items:center">
            <div class="arrow" style="font-size:44px;line-height:1">← ответ</div>
            <div class="msg">{"title": "Брат", "year": 1997}</div></div>
        </div>
        <div class="card flowbox" style="flex:none;width:330px;height:260px"><div style="font-size:70px">🗄️</div>
          <h3 style="margin-top:8px">Сервер API</h3><p>ищет фильм у себя в базе</p></div>
      </div>
      <div class="card" style="flex:none;padding:22px 30px"><p><b>API</b> — способ, которым одна программа просит данные
      у другой. Как официант в кафе: ты не идёшь на кухню, а делаешь заказ — и тебе приносят блюдо.</p></div></div>"""
    return slide("Что такое <em>API</em>", body, n)


def s_blocks(n):
    blocks = [
        ("97", "История", "факты и правители"),
        ("85", "Кулинария", "блюда и повара"),
        ("106", "Кино", "фильмы, режиссёры, актёры"),
        ("160", "Города", "страны, города, достопри&shy;мечательности"),
        ("86", "Книги", "книги и авторы"),
    ]
    cards = "".join(
        f'<div class="card" style="padding:26px 24px"><div class="gnum">{num}</div>'
        f'<div style="font-size:19px;font-weight:700;color:var(--text);margin:6px 0 16px">записей</div>'
        f'<h3>{h}</h3><p style="font-size:21px">{p}</p></div>'
        for num, h, p in blocks
    )
    body = f"""<div class="col" style="height:100%;gap:26px">
      <div class="row" style="height:auto;gap:22px">{cards}</div>
      <p class="lead" style="font-size:28px">Всего <em>534 записи</em> и <em>85 адресов</em>.
      У большинства записей есть картинка — для бота с фото самое то.</p></div>"""
    return slide("Что есть в <em>нашем API</em>", body, n)


def s_url(n):
    parts = [
        (f"http://{EXAMPLE_IP}", "p1", "где сервер"),
        (":8085", "p2", "порт"),
        ("/api/movies", "p3", "блок данных"),
        ("/random_movie", "p4", "что хотим"),
    ]
    segs = "".join(
        f'<div class="seg"><div class="part {c}">{t}</div><div class="lbl">{lbl}</div></div>'
        for t, c, lbl in parts
    )
    examples = [
        ("/api/historic/random_fact", "случайный исторический факт"),
        ("/api/cooking/dishes/by_type/Суп", "все супы"),
        ("/api/books/search_books?query=Пушкин", "поиск книг и авторов"),
    ]
    ex = "".join(
        f'<div class="card sm" style="padding:20px 24px"><div class="ep" style="margin:0 0 8px;font-size:18px">'
        f"{u}</div><p>{t}</p></div>"
        for u, t in examples
    )
    body = f"""<div class="col" style="height:100%;gap:44px">
      <div class="url" style="margin-top:16px">{segs}</div>
      <p class="lead" style="font-size:28px">Меняешь конец адреса — сервер отвечает другими данными:</p>
      <div class="row" style="height:auto;gap:22px">{ex}</div></div>"""
    return slide("Адрес — это <em>вопрос</em> серверу", body, n)


def s_json(n):
    js = """{
  <span class="n">"title"</span>: <span class="s">"Иван Васильевич меняет профессию"</span>,
  <span class="n">"year"</span>: 1973,
  <span class="n">"director"</span>: <span class="s">"Леонид Гайдай"</span>,
  <span class="n">"genre"</span>: <span class="s">"Комедия"</span>,
  <span class="n">"rating"</span>: 8.8,
  <span class="n">"actors"</span>: [<span class="s">"Александр Демьяненко"</span>, ...],
  <span class="n">"img_url"</span>: <span class="s">"https://..."</span>
}"""
    py = """movie = response.json()

movie[<span class="s">"title"</span>]
<span class="c"># Иван Васильевич меняет профессию</span>

movie[<span class="s">"actors"</span>][<span class="n">0</span>]
<span class="c"># Александр Демьяненко</span>"""
    body = f"""<div class="row" style="align-items:flex-start">
      <div class="col" style="flex:none;width:720px;gap:14px"><div class="chip" style="align-self:flex-start">приходит от сервера</div>
        <div class="code" style="font-size:21px;padding:26px 30px">{js}</div></div>
      <div class="col" style="flex:1;gap:14px"><div class="chip" style="align-self:flex-start">в Python это словарь</div>
        <div class="code" style="font-size:21px;padding:26px 30px">{py}</div>
        <p class="txt" style="font-size:22px">JSON — текст, похожий на словарь Python. <b>.json()</b> превращает его
        в настоящий словарь.</p></div></div>"""
    return slide("Ответ приходит в <em>JSON</em>", body, n)


def s_first(n):
    code = f"""<span class="k">import</span> requests

API = <span class="s">"http://{EXAMPLE_IP}:8085"</span>  <span class="c"># адрес с доски</span>

movie = requests.get(<span class="s">f"{{API}}/api/movies/random_movie"</span>).json()
print(movie[<span class="s">"title"</span>], movie[<span class="s">"year"</span>])"""
    body = f"""<div class="row"><div class="col" style="flex:none;width:880px">
      <div class="code" style="font-size:22px">{code}</div>
      <p class="txt">Запусти — и в консоли появится случайный фильм. Запусти ещё раз — будет другой.</p></div>
      <div class="col sm" style="flex:1;gap:18px">
        <div class="card" style="flex:none;padding:18px 22px"><h3>/docs</h3><p>Все адреса API с кнопкой «Try it out» —
        пробуй прямо в браузере.</p></div>
        <div class="card" style="flex:none;padding:18px 22px"><h3>ID — строки</h3><p><span class="mono">movies["1"]</span>,
        а не <span class="mono">movies[1]</span></p></div>
        <div class="card" style="flex:none;padding:18px 22px"><h3>title или name</h3><p>У фильмов и книг —
        <span class="mono">title</span>, у остальных — <span class="mono">name</span></p></div></div></div>"""
    return slide("Первый <em>запрос</em>", body, n)


def s_bot(n):
    phone = """<div class="tg"><div class="bar"><div class="ava">К</div><div>Кино-бот<small>бот</small></div></div>
      <div class="chat"><div class="bub me">/movie</div>
      <div class="bub bot"><img src="assets/movie.jpg"><div><b>Иван Васильевич меняет профессию (1973)</b><br>
      Рейтинг: 8.8<br><br><span style="color:#55607a">Инженер Тимофеев изобретает машину времени…</span></div></div>
      </div></div>"""
    code = """<span class="k">@bot.message_handler</span>(commands=[<span class="s">"movie"</span>])
<span class="k">def</span> random_movie(message):
    movie = requests.get(<span class="s">f"{API}/api/movies/random_movie"</span>).json()
    text = <span class="s">f"{movie['title']} ({movie['year']})"</span>
    <span class="k">try</span>:
        bot.send_photo(message.chat.id, movie[<span class="s">"img_url"</span>], caption=text)
    <span class="k">except</span> Exception:
        bot.send_message(message.chat.id, text)  <span class="c"># нет картинки</span>"""
    body = f"""<div class="row" style="gap:40px">{phone}
      <div class="col" style="flex:1;min-width:0;gap:18px">
        <div class="code" style="font-size:17.5px;padding:24px 26px">{code}</div>
        <div class="row sm" style="height:auto;gap:18px">
          <div class="card" style="padding:16px 22px"><h3>Библиотека</h3><p><span class="mono">pip install
          pyTelegramBotAPI</span></p></div>
          <div class="card" style="padding:16px 22px"><h3>Токен</h3><p>Создай бота у <b>@BotFather</b> и вставь
          токен в код</p></div></div>
        <p class="txt" style="font-size:21px">Шаблон: <span class="mono">examples/bot_example.py</span></p></div></div>"""
    return slide("Трек 1: <em>Telegram-бот</em>", body, n)


def s_qt(n):
    window = """<div class="win"><div class="tbar"><span class="dot" style="background:#ff5f57"></span>
      <span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>
      <span style="margin-left:8px">Случайный фильм</span></div>
      <img src="assets/qt_app.png" style="width:504px"></div>"""
    code = """HEADERS = {<span class="s">"User-Agent"</span>: <span class="s">"ShctHackathonApp/1.0"</span>}

<span class="k">def</span> show_movie(self):
    movie = requests.get(<span class="s">f"{API}/api/movies/random_movie"</span>).json()
    self.text.setText(movie[<span class="s">"title"</span>])
    <span class="hl">data = requests.get(movie[<span class="s">"img_url"</span>], headers=HEADERS).content</span>
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    self.picture.setPixmap(pixmap.scaledToWidth(<span class="n">300</span>))"""
    body = f"""<div class="row" style="gap:40px;align-items:flex-start">{window}
      <div class="col" style="flex:1;min-width:0;gap:18px">
        <div class="code" style="font-size:16.5px;padding:24px 26px">{code}</div>
        <div class="card sm" style="flex:none;padding:16px 22px"><h3>Не забудь headers</h3><p>Без заголовка
        <span class="mono">User-Agent</span> половина картинок не загрузится: Wikimedia ответит ошибкой 403.</p></div>
        <p class="txt" style="font-size:21px"><span class="mono">pip install PyQt6</span> · шаблон:
        <span class="mono">examples/qt_example.py</span></p></div></div>"""
    return slide("Трек 2: <em>Qt-приложение</em>", body, n)


def s_choose(n):
    def card(title, chip, pros, cons):
        items = "".join(f'<div class="plus"><b>+</b><span>{p}</span></div>' for p in pros)
        items += "".join(f'<div class="minus"><b>−</b><span>{c}</span></div>' for c in cons)
        return (
            f'<div class="card col" style="gap:18px"><div class="chip" style="align-self:flex-start">{chip}</div>'
            f"<h3>{title}</h3>{items}</div>"
        )

    bot = card(
        "Telegram-бот",
        "быстрый результат",
        ["Пишешь боту с телефона, как другу", "Легко показать на демо и друзьям", "Кнопки прямо в чате"],
        ["Нужен токен и Telegram в сети школы"],
    )
    qt = card(
        "Qt-приложение",
        "для любителей интерфейсов",
        ["Своё окно: кнопки, списки, картинки", "Работает без Telegram", "Можно сделать красиво"],
        ["Картинкам нужен заголовок User-Agent"],
    )
    body = f"""<div class="col" style="height:100%;gap:22px"><div class="row" style="flex:1">{bot}{qt}</div>
      <p class="txt">Данные одни и те же, и оцениваются оба трека <b>одинаково</b>. Выбирай то, что интереснее.</p></div>"""
    return slide("Какой трек <em>выбрать</em>?", body, n)


def s_ideas(n):
    ideas = [
        ("Кино-рулетка", "★", "Случайный фильм с постером", "/random_movie"),
        ("Факт дня", "★", "Исторический факт по команде", "/random_fact"),
        ("Что приготовить?", "★★", "Блюда до 20 минут или по типу", "/dishes/quick<br>/dishes/by_type/Суп"),
        ("Угадай год", "★★", "Викторина: 4 варианта ответа", "/random_movie<br>/titles_of_all_movies"),
        ("Путеводитель", "★★★", "Страна → города → места", "/cities_by_country/…<br>/landmarks_by_city/…"),
        ("Викторина на время", "★★★", "Таймер и таблица рекордов", "любые random_*"),
    ]
    cards = "".join(
        f'<div class="card sm" style="padding:22px 24px;min-height:200px"><div style="display:flex;justify-content:space-between;'
        f'align-items:baseline"><h3>{t}</h3><span class="stars">{s}</span></div><p>{d}</p>'
        f'<div class="ep">{e}</div></div>'
        for t, s, d, e in ideas
    )
    body = f"""<div class="col" style="gap:30px"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px">
      {cards}</div><p class="txt">★ — справится новичок, ★★★ — для опытных. Можно придумать своё: главное, чтобы
      программа брала данные из API.</p></div>"""
    return slide("Идеи <em>проектов</em>", body, n)


def s_levels(n):
    levels = [
        ("Данные", "Покажи запись из API текстом"),
        ("Картинка", "Добавь фото из img_url"),
        ("Кнопки", "Меню или кнопки вместо команд"),
        ("Ввод", "Фильтр или поиск по запросу пользователя"),
        ("Надёжность", "Не падает на 404 и пустой картинке"),
        ("Своя фишка", "Очки, избранное, таймер — то, чего нет в API"),
    ]
    cards = "".join(
        f'<div class="card" style="height:{210 + i * 56}px"><div class="num">{i + 1}</div>'
        f"<h3>{h}</h3><p>{p}</p></div>"
        for i, (h, p) in enumerate(levels)
    )
    body = f"""<div class="stairs">{cards}</div>"""
    return slide("Уровни <em>прокачки</em>", body, n)


def s_errors(n):
    errs = [
        ("ConnectionError", "Проверь адрес: не <b>localhost</b>, а адрес с доски. Открой /ping в браузере."),
        ("KeyError: 1", "ID — строки: <span class='mono'>movies[\"1\"]</span>"),
        ("KeyError: 'name'", "У фильмов и книг поле называется <span class='mono'>title</span>"),
        ("404 Not Found", "Такого нет. Посмотри в <b>/docs</b>, какие значения бывают."),
        ("Бот упал на send_photo", "Не у всех записей есть картинка — оберни в <b>try/except</b>."),
        ("Нет картинки в Qt", "Добавь <span class='mono'>headers=HEADERS</span> в requests.get"),
    ]
    cards = "".join(
        f'<div class="card err" style="padding:22px 24px;min-height:150px"><h3>{e}</h3><p>{f}</p></div>' for e, f in errs
    )
    body = f"""<div class="col" style="gap:30px"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px">
      {cards}</div><div class="card" style="flex:none;padding:20px 28px"><p><b>Первым делом</b> открой тот же адрес
      в браузере. Видишь JSON — сервер в порядке, ищи ошибку в коде.</p></div></div>"""
    return slide("Частые <em>ошибки</em>", body, n)


def s_score(n):
    crit = [("Работает", 30), ("Использование API", 20), ("Удобство", 20), ("Идея и фишка", 15), ("Презентация", 15)]
    bars = "".join(
        f'<div class="b"><span>{c}</span><div class="track"><div class="fill" style="width:{p / 30 * 100:.0f}%">'
        f'</div></div><span class="pts">{p}</span></div>'
        for c, p in crit
    )
    body = f"""<div class="row"><div class="col" style="flex:1.3;justify-content:center"><div class="bars">{bars}</div>
      <p class="txt" style="margin-top:6px">Всего 100 баллов от каждого члена жюри.</p></div>
      <div class="col" style="flex:1;justify-content:center"><div class="card" style="flex:none"><h3>Демо — 3 минуты</h3><p><b>1.</b> Что за проект и для кого<br>
      <b>2.</b> Покажи вживую<br><b>3.</b> Чем гордишься больше всего</p></div>
      <div class="card" style="flex:none;padding:20px 26px"><h3 style="font-size:26px">Номинации</h3><p style="font-size:21px">
      Самый полезный · Самый смешной · Лучший интерфейс · Лучший первый проект</p></div></div></div>"""
    return slide("Как <em>оценим</em>", body, n)


def s_day(n):
    stops = [
        ("10:00", "Открытие", ""),
        ("10:20", "Первый запрос", ""),
        ("10:40", "Команды и идеи", ""),
        ("11:00", "Работа", "чекпоинт 12:00"),
        ("13:00", "Обед", ""),
        ("13:40", "Работа", "чекпоинт 14:30"),
        ("15:30", "Стоп-код", ""),
        ("15:45", "Демо", ""),
        ("16:45", "Награждение", ""),
    ]
    step = (1296 - 144) / (len(stops) - 1)
    html = "".join(
        f'<div class="stop{" on" if cp else ""}" style="left:{i * step:.0f}px"><div class="t">{t}</div>'
        f'<div class="d"></div><div class="w">{w}</div>{f"<div class=cp>{cp}</div>" if cp else ""}</div>'
        for i, (t, w, cp) in enumerate(stops)
    )
    body = f"""<div class="col" style="height:100%;gap:40px;padding-top:30px">
      <div class="tl" style="height:290px"><div class="line" style="left:72px;right:72px"></div>{html}</div>
      <div class="card" style="flex:none;padding:20px 28px"><p>На чекпоинтах ментор подходит к каждой команде.
      Цель к <b>12:00</b> — программа показывает данные из API. К <b>14:30</b> — есть кнопки или фильтр.</p></div></div>"""
    return slide("Как пройдёт <em>день</em>", body, n)


def s_go(n):
    host = SERVER or '<span style="display:inline-block;width:250px"></span>'
    body = f"""<div class="row" style="align-items:center"><div class="col" style="flex:1;gap:30px">
      <h1 style="font-size:110px">Погнали!</h1>
      <p class="lead" style="color:#fff">Открой браузер и проверь, что сервер отвечает.</p></div>
      <div class="card col" style="flex:1.25;gap:20px;padding:36px 40px">
        <p style="font-size:24px;font-weight:700">Адрес сервера</p>
        <div style="white-space:nowrap"><span class="addr">http://{host}:8085</span></div>
        <p style="font-size:24px;margin-top:10px"><b class="mono">/ping</b> — проверка, ответ <span class="mono">"PONG!"</span><br>
        <b class="mono">/docs</b> — все адреса API<br><b class="mono">examples/</b> — шаблоны бота и Qt</p></div></div>"""
    return slide("Время <em>писать код</em>", body, n, cls="grad")


SLIDES = [
    s_plan, s_api, s_blocks, s_url, s_json, s_first, s_bot, s_qt,
    s_choose, s_ideas, s_levels, s_errors, s_score, s_day, s_go,
]


def build_html(extra_css=""):
    pages = [s_title()] + [fn(i + 2) for i, fn in enumerate(SLIDES)]
    return (
        '<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="assets/fonts/fonts.css">'
        f"<style>{CSS}{CSS_EXTRA}{extra_css}</style></head>"
        f'<body class="t-shct">{"".join(pages)}</body></html>'
    )


def chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return str(c)
    sys.exit("Не найден Chromium: укажите путь в переменной CHROME")


def run_chrome(*args):
    base = [chrome(), "--headless", "--disable-gpu", "--allow-file-access-from-files",
            "--virtual-time-budget=4000", "--hide-scrollbars"]
    subprocess.run(base + list(args), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    html_path = HERE / f"{OUT}.html"
    html_path.write_text(build_html(), encoding="utf-8")
    run_chrome("--no-pdf-header-footer", f"--print-to-pdf={HERE / OUT}.pdf", html_path.as_uri())
    print("готово:", f"{OUT}.html", f"{OUT}.pdf")

    if "--preview" in sys.argv:
        prev = HERE / "preview"
        prev.mkdir(exist_ok=True)
        for i in range(1, len(SLIDES) + 2):
            tmp = HERE / f".preview_{i}.html"
            css = f".slide{{display:none}} .slide:nth-of-type({i}){{display:block}}"
            tmp.write_text(build_html(css), encoding="utf-8")
            run_chrome("--window-size=1440,810", f"--screenshot={prev / f'slide_{i:02d}.png'}", tmp.as_uri())
            tmp.unlink()
        print("превью:", prev)


if __name__ == "__main__":
    main()
