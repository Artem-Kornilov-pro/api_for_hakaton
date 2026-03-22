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
        "img_url": "https://avatars.mds.yandex.net/i?id=8238cb89d8df1a7e258957fe6ddbf195_l-9053276-images-thumbs&n=13",
    },
    "2": {
        "year": 1380,
        "title": "Куликовская битва",
        "fact": "Куликовская битва",
        "description": "Сражение между русскими войсками под предводительством Дмитрия Донского и монголо-татарскими войсками Мамая.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1974877/1250098087/S600xU_2x",
    },
    "3": {
        "year": 862,
        "title": "Призвание варягов",
        "fact": "Начало династии Рюриковичей",
        "description": "Славянские племена призвали варягов для княжения, что считается началом российской государственности.",
        "img_url": "https://avatars.mds.yandex.net/i?id=db17c5eb65bbfd029da6931a647acf44_sr-5302491-images-thumbs&n=13",
    },
    "4": {
        "year": 988,
        "title": "Крещение Руси",
        "fact": "Владимир Красное Солнышко крестил Русь",
        "description": "Князь Владимир принял христианство и крестил Киевскую Русь, что определило культурное развитие страны на века.",
        "img_url": "https://media.pravoslavie.ru/469808.s.jpg",
    },
    "5": {
        "year": 1240,
        "title": "Невская битва",
        "fact": "Александр Невский разбил шведов",
        "description": "Молодой князь Александр Ярославич одержал победу над шведским войском, получив прозвище 'Невский'.",
        "img_url": "https://cdn.tvspb.ru/storage/wp-content/uploads/2022/06/p1bkmmyzsmdthumbnail_rAszbEG.jpg__0_0x0.jpg",
    },
    "6": {
        "year": 1703,
        "title": "Основание Санкт-Петербурга",
        "fact": "Петр I основал новую столицу",
        "description": "Петр Первый заложил Петропавловскую крепость, с чего началось строительство Санкт-Петербурга.",
        "img_url": "https://avatars.mds.yandex.net/i?id=86b6972d54c96ea9927fa5e971e069e19b85f636-4719550-images-thumbs&n=13",
    },
    "7": {
        "year": 1812,
        "title": "Бородинское сражение",
        "fact": "Крупнейшее сражение Отечественной войны 1812 года",
        "description": "Генеральное сражение между русской армией Кутузова и французской армией Наполеона под Москвой.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2038203/1237550538/S600xU_2x",
    },
    "8": {
        "year": 1861,
        "title": "Отмена крепостного права",
        "fact": "Александр II освободил крестьян",
        "description": "Император Александр II подписал манифест об отмене крепостного права в России.",
        "img_url": "https://i0.wp.com/gsrussia.ru/wp-content/uploads/2022/12/image-16.png",
    },
    "9": {
        "year": 1961,
        "title": "Первый полет в космос",
        "fact": "Гагарин стал первым человеком в космосе",
        "description": "Юрий Гагарин на корабле 'Восток-1' совершил первый в истории полет в космическое пространство.",
        "img_url": "https://rgantd.ru/upload/resize_cache/iblock/3e9/500_500_1/3lucha9bdp06bjvu71rbizts562vj7hs.jpg",
    },
    "10": {
        "year": 1945,
        "title": "День Победы",
        "fact": "Окончание Великой Отечественной войны",
        "description": "Подписание акта о безоговорочной капитуляции Германии ознаменовало победу СССР в войне.",
        "img_url": "https://avatars.mds.yandex.net/i?id=2c7291cb637dd5c15aa770fa60c61d852be09bb0-5865432-images-thumbs&n=13",
    },
    "11": {
        "year": 1223,
        "title": "Битва на Калке",
        "fact": "Первое столкновение Руси с монголами",
        "description": "Первое сражение между объединённым русско-половецким войском и монгольской армией. Поражение русских князей стало предвестником монгольского нашествия.",
        "img_url": "https://avatars.mds.yandex.net/i?id=50b23fca34b903d21ce3f6623c5d65e91baf87b3-9404058-images-thumbs&n=13",
    },
    "12": {
        "year": 1237,
        "title": "Нашествие Батыя",
        "fact": "Начало монголо-татарского ига",
        "description": "Монгольское войско под предводительством хана Батыя вторглось на Русь. Были захвачены и разорены Рязань, Владимир, Киев и другие города. Начался период ордынского владычества.",
        "img_url": "",
    },
    "13": {
        "year": 1552,
        "title": "Взятие Казани",
        "fact": "Иван Грозный присоединил Казанское ханство",
        "description": "Русские войска под предводительством Ивана Грозного после осады взяли Казань. Казанское ханство было присоединено к России, что положило начало освоению Поволжья.",
        "img_url": "https://avatars.mds.yandex.net/i?id=1477d3263141783da3ddfccc0c030e3353bb01b6-4310964-images-thumbs&n=13",
    },
    "14": {
        "year": 1581,
        "title": "Начало освоения Сибири",
        "fact": "Поход Ермака",
        "description": "Казачий атаман Ермак Тимофеевич начал поход в Сибирь. Это событие положило начало присоединению Сибири к Русскому государству.",
        "img_url": "https://avatars.mds.yandex.net/i?id=20d4f984c704ff152425246d0c6d0bfb3e52fc28-5163185-images-thumbs&n=13",
    },
    "15": {
        "year": 1612,
        "title": "Освобождение Москвы",
        "fact": "Окончание Смутного времени",
        "description": "Народное ополчение под руководством Минина и Пожарского освободило Москву от польских интервентов. Это событие положило конец Смутному времени.",
        "img_url": "https://avatars.mds.yandex.net/i?id=35c019c8ae9a1be42175960b679e1a293bb903ed-9202550-images-thumbs&n=13",
    },
    "16": {
        "year": 1709,
        "title": "Полтавская битва",
        "fact": "Разгром шведской армии",
        "description": "Решающее сражение Северной войны, в котором русская армия под командованием Петра I разгромила шведскую армию Карла XII. После этой победы Россия стала великой европейской державой.",
        "img_url": "https://avatars.mds.yandex.net/i?id=eccac37d370a49c8809e98eb0298bd81050f2cea-9870394-images-thumbs&n=13",
    },
    "17": {
        "year": 1773,
        "title": "Восстание Пугачёва",
        "fact": "Крестьянская война",
        "description": "Крупнейшее в истории России крестьянское восстание под предводительством Емельяна Пугачёва. Охватило огромные территории и было жестоко подавлено правительственными войсками.",
        "img_url": "https://avatars.mds.yandex.net/i?id=43f74ba3e74f58a68d5dd2aef1f643120f510525-6903367-images-thumbs&n=13",
    },
    "18": {
        "year": 1853,
        "title": "Синопское сражение",
        "fact": "Последнее крупное сражение парусных флотов",
        "description": "Русская эскадра под командованием адмирала Нахимова уничтожила турецкий флот в Синопской бухте. Это сражение стало поводом для вступления Англии и Франции в Крымскую войну.",
        "img_url": "https://avatars.mds.yandex.net/i?id=159ffbe553e9c6d4d15778dfe6f5b60d0100e52d-4471740-images-thumbs&n=13",
    },
    "19": {
        "year": 1905,
        "title": "Кровавое воскресенье",
        "fact": "Начало Первой русской революции",
        "description": "Расстрел мирного шествия рабочих к Зимнему дворцу. Это событие стало началом Первой русской революции 1905-1907 годов.",
        "img_url": "https://avatars.mds.yandex.net/i?id=09b78478de5f2ec734dd9f5a34b0e67f1476e803-5233576-images-thumbs&n=13",
    },
    "20": {
        "year": 1918,
        "title": "Расстрел царской семьи",
        "fact": "Гибель Николая II и его семьи",
        "description": "В Екатеринбурге в подвале дома Ипатьева были расстреляны последний российский император Николай II, его жена и пятеро детей.",
        "img_url": "https://avatars.mds.yandex.net/i?id=69b0c1af3ec0b90d36fc16f98e1fa31030d7f005-5869150-images-thumbs&n=13",
    },
    "21": {
        "year": 1937,
        "title": "Первый полёт через Северный полюс",
        "fact": "Экипаж Чкалова совершил беспосадочный перелёт",
        "description": "Валерий Чкалов, Георгий Байдуков и Александр Беляков совершили беспосадочный перелёт Москва — Северный полюс — США, установив мировой рекорд дальности полёта.",
        "img_url": "https://avatars.mds.yandex.net/i?id=6dcf6f82bff1b71c54a6a8de1bd1df5a10e157ec3458ce6a-12508201-images-thumbs&n=13",
    },
    "22": {
        "year": 1957,
        "title": "Запуск первого спутника",
        "fact": "Начало космической эры",
        "description": "С космодрома Байконур был запущен первый в мире искусственный спутник Земли. Это событие открыло космическую эру в истории человечества.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2265709/1245030265/SUx182",
    },
    "23": {
        "year": 1965,
        "title": "Первый выход в открытый космос",
        "fact": "Алексей Леонов вышел в открытый космос",
        "description": "Космонавт Алексей Леонов в ходе полёта корабля 'Восход-2' впервые в истории вышел в открытый космос. Пребывание за бортом корабля составило 12 минут 9 секунд.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2403345/1250053822/SUx182_2x",
    },
    "24": {
        "year": 1980,
        "title": "Московская Олимпиада",
        "fact": "Летние Олимпийские игры в Москве",
        "description": "В Москве прошли XXII летние Олимпийские игры. Они стали первыми Олимпийскими играми, проведёнными в социалистической стране.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2304191/1227232147/S600xU_2x",
    },
    "25": {
        "year": 2014,
        "title": "Олимпиада в Сочи",
        "fact": "Зимние Олимпийские игры в России",
        "description": "В Сочи прошли XXII зимние Олимпийские игры. Российская сборная завоевала рекордное количество медалей и заняла первое место в общем зачёте.",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2069560/823213801/SUx182_2x",
    },
}

# Новая база данных о правителях
rulers = {
    "1": {
        "name": "Рюрик",
        "years_rule": "862-879",
        "dynasty": "Рюриковичи",
        "facts": [
            "Основатель династии Рюриковичей",
            "Первый новгородский князь",
            "Призван на княжение славянскими племенами",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/5528860/1248304069/S600xU_2x",
        "important_event": "Призвание варягов и начало княжения в Новгороде",
    },
    "2": {
        "name": "Владимир Святославич (Красное Солнышко)",
        "years_rule": "980-1015",
        "dynasty": "Рюриковичи",
        "facts": [
            "Крестил Русь в 988 году",
            "Объединил все восточнославянские земли",
            "При нем началась чеканка монет",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2223725/1174719715/S600xU_2x",
        "important_event": "Крещение Руси",
    },
    "3": {
        "name": "Ярослав Мудрый",
        "years_rule": "1019-1054",
        "dynasty": "Рюриковичи",
        "facts": [
            "Составил первый свод законов 'Русская правда'",
            "При нем Киев стал одним из крупнейших городов Европы",
            "Основал библиотеку в Софийском соборе",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/4785917/1245008196/S600xU_2x",
        "important_event": "Расцвет Киевской Руси и создание 'Русской правды'",
    },
    "4": {
        "name": "Александр Невский",
        "years_rule": "1252-1263",
        "dynasty": "Рюриковичи",
        "facts": [
            "Победил шведов в Невской битве (1240)",
            "Разбил немецких рыцарей в Ледовом побоище (1242)",
            "Причислен к лику святых",
        ],
        "img_url": "https://www.pravmir.ru/wp-content/uploads/2012/09/826_59-768x995.jpeg",
        "important_event": "Защита северо-западных рубежей Руси от крестоносцев",
    },
    "5": {
        "name": "Иван III Васильевич",
        "years_rule": "1462-1505",
        "dynasty": "Рюриковичи",
        "facts": [
            "Сверг монголо-татарское иго (1480)",
            "Принял титул 'Государь всея Руси'",
            "Построил Московский Кремль из красного кирпича",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/5504037/1237254929/S600xU_2x",
        "important_event": "Стояние на реке Угре - конец ордынского ига",
    },
    "6": {
        "name": "Иван IV Грозный",
        "years_rule": "1533-1584",
        "dynasty": "Рюриковичи",
        "facts": [
            "Первый венчанный на царство царь (1547)",
            "Присоединил Казанское и Астраханское ханства",
            "Начало освоения Сибири",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/10843572/1244157545/S600xU_2x",
        "important_event": "Венчание на царство и начало реформ",
    },
    "7": {
        "name": "Петр I Великий",
        "years_rule": "1682-1725",
        "dynasty": "Романовы",
        "facts": [
            "Провел масштабные реформы",
            "Основал Санкт-Петербург",
            "Создал российский флот",
            "Провел губернскую реформу",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2114485/1247603534/S600xU_2x",
        "important_event": "Основание Санкт-Петербурга и провозглашение России империей",
    },
    "8": {
        "name": "Екатерина II Великая",
        "years_rule": "1762-1796",
        "dynasty": "Романовы",
        "facts": [
            "Присоединила Крым и Новороссию",
            "Провела губернскую реформу",
            "Основала Эрмитаж",
            "Переписывалась с Вольтером",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2368666/1237485367/S600xU_2x",
        "important_event": "Присоединение Крыма и развитие просвещения",
    },
    "9": {
        "name": "Александр II Освободитель",
        "years_rule": "1855-1881",
        "dynasty": "Романовы",
        "facts": [
            "Отменил крепостное право (1861)",
            "Провел военную реформу",
            "Продал Аляску США (1867)",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2363292/1247705158/S600xU_2x",
        "important_event": "Отмена крепостного права",
    },
    "10": {
        "name": "Николай II",
        "years_rule": "1894-1917",
        "dynasty": "Романовы",
        "facts": [
            "Последний российский император",
            "Отрекся от престола в 1917 году",
            "Расстрелян с семьей в 1918 году",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2295215/1247693461/S600xU_2x",
        "important_event": "Февральская революция и отречение от престола",
    },
    "11": {
        "name": "Владимир Ильич Ленин (Ульянов)",
        "years_rule": "1917-1924",
        "dynasty": "Советские лидеры",
        "facts": [
            "Основатель Советского государства",
            "Руководитель Октябрьской революции 1917 года",
            "Создатель Коммунистической партии и Коминтерна",
            "Инициатор политики 'военного коммунизма' и НЭПа",
        ],
        "img_url": "https://avatars.mds.yandex.net/i?id=e1a5a0d96767e39342edb108f8cb104f819b5fc4-4379638-images-thumbs&n=13",
        "important_event": "Октябрьская революция и создание СССР",
    },
    "12": {
        "name": "Иосиф Виссарионович Сталин (Джугашвили)",
        "years_rule": "1924-1953",
        "dynasty": "Советские лидеры",
        "facts": [
            "Руководитель СССР в годы индустриализации и коллективизации",
            "Верховный главнокомандующий в Великой Отечественной войне",
            "Один из лидеров антигитлеровской коалиции",
            "Инициатор создания атомной бомбы в СССР",
        ],
        "img_url": "https://avatars.mds.yandex.net/i?id=7e7eac2fcf8ff745914abe0e3e39c546f86f190a-4888009-images-thumbs&n=13",
        "important_event": "Победа в Великой Отечественной войне и превращение СССР в сверхдержаву",
    },
    "13": {
        "name": "Никита Сергеевич Хрущёв",
        "years_rule": "1953-1964",
        "dynasty": "Советские лидеры",
        "facts": [
            "Инициатор 'оттепели' и разоблачения культа личности Сталина",
            "Запустил первый искусственный спутник Земли",
            "Начал массовое строительство жилья ('хрущёвки')",
            "Выступал в ООН с известным 'кузькиной матерью'",
        ],
        "img_url": "https://gbousosh8.minobr63.ru/wordpress/wp-content/uploads/Хрущев.jpg",
        "important_event": "Начало освоения космоса и хрущёвская оттепель",
    },
    "14": {
        "name": "Леонид Ильич Брежнев",
        "years_rule": "1964-1982",
        "dynasty": "Советские лидеры",
        "facts": [
            "Период его правления называют 'эпохой застоя'",
            "При нём была принята Конституция 1977 года",
            "Активно развивал космическую программу и ВПК",
            "Любил охоту и автомобили",
        ],
        "img_url": "https://avatars.mds.yandex.net/i?id=52b1b23097cd9fe3a1484c96e573ab12ea7b0f3d-17508662-images-thumbs&n=13",
        "important_event": "Эпоха развитого социализма и достижение военного паритета с США",
    },
    "15": {
        "name": "Михаил Сергеевич Горбачёв",
        "years_rule": "1985-1991",
        "dynasty": "Советские лидеры",
        "facts": [
            "Инициатор перестройки и гласности",
            "Лауреат Нобелевской премии мира",
            "Последний Генеральный секретарь ЦК КПСС",
            "При нём произошёл распад СССР",
        ],
        "img_url": "https://avatars.mds.yandex.net/i?id=22aa58ad0b2da5e2dd078c27b2cfef3b621f9aab-5333360-images-thumbs&n=13",
        "important_event": "Перестройка и окончание холодной войны",
    },
    "16": {
        "name": "Борис Николаевич Ельцин",
        "years_rule": "1991-1999",
        "dynasty": "Президенты РФ",
        "facts": [
            "Первый президент Российской Федерации",
            "Инициатор рыночных реформ и приватизации",
            "Автор Конституции 1993 года",
            "Известен фразой 'Я устал, я ухожу'",
        ],
        "img_url": "https://avatars.mds.yandex.net/i?id=d0bbe359a0b2c8c14447490a028dfc4bd82e35ab-5877852-images-thumbs&n=13",
        "important_event": "Становление новой России и переход к рыночной экономике",
    },
    "17": {
        "name": "Владимир Владимирович Путин",
        "years_rule": "2000-2008, 2012-наст. время",
        "dynasty": "Президенты РФ",
        "facts": [
            "Второй и четвёртый президент России",
            "Самый долго правящий руководитель после Сталина",
            "Имеет чёрный пояс по дзюдо",
            "Кандидат экономических наук",
        ],
        "img_url": "https://cdn.ananasposter.ru/image/cache/catalog/poster/pos24/11/84065-1000x830.jpg",
        "important_event": "Укрепление государственности и возвращение Крыма",
    },
    "18": {
        "name": "Дмитрий Анатольевич Медведев",
        "years_rule": "2008-2012",
        "dynasty": "Президенты РФ",
        "facts": [
            "Третий президент России",
            "Инициатор модернизации и цифровизации",
            "Запустил проект 'Сколково'",
            "Активный пользователь социальных сетей",
        ],
        "img_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Дмитрий_Медведев_%2808-04-2022%29.jpg/960px-Дмитрий_Медведев_%2808-04-2022%29.jpg",
        "important_event": "Президентский срок и программа модернизации",
    },
    "19": {
        "name": "Алексей Михайлович Романов (Тишайший)",
        "years_rule": "1645-1676",
        "dynasty": "Романовы",
        "facts": [
            "Второй царь из династии Романовых",
            "При нём произошло воссоединение Украины с Россией",
            "Провёл церковную реформу патриарха Никона",
            "Отец Петра I",
        ],
        "img_url": "https://cdn.monetnik.ru/storage/blog/d2pzz8a614/2024-12-2801.800.jpg",
        "important_event": "Соборное уложение 1649 года и укрепление самодержавия",
    },
    "20": {
        "name": "Анна Иоанновна",
        "years_rule": "1730-1740",
        "dynasty": "Романовы",
        "facts": [
            "Императрица всероссийская, племянница Петра I",
            "Известна своим фаворитом Бироном и 'бироновщиной'",
            "Любила стрельбу и шутов",
            "При ней открыт первый кадетский корпус",
        ],
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1880293/1245057186/S600xU_2x",
        "important_event": "Правление с опорой на немецких дворян",
    },
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
    dynasty_rulers = {
        id: ruler for id, ruler in rulers.items() if ruler["dynasty"].lower() == dynasty.lower()
    }
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
    # Подсчёт правителей по династиям/эпохам
    dynasties_count = {}
    for ruler in rulers.values():
        dynasty = ruler["dynasty"]
        dynasties_count[dynasty] = dynasties_count.get(dynasty, 0) + 1

    # Самый старый и самый новый факт
    facts_list = list(historic_facts.values())
    oldest_fact = min(facts_list, key=lambda x: x["year"]) if facts_list else None
    newest_fact = max(facts_list, key=lambda x: x["year"]) if facts_list else None

    # Самый старый и самый новый правитель (по началу правления)
    rulers_list = list(rulers.values())

    # Функция для извлечения года начала правления
    def get_start_year(ruler):
        try:
            return int(ruler["years_rule"].split("-")[0])
        except:
            return 0

    oldest_ruler = min(rulers_list, key=get_start_year) if rulers_list else None
    newest_ruler = max(rulers_list, key=get_start_year) if rulers_list else None

    stats = {
        "total_facts": len(historic_facts),
        "total_rulers": len(rulers),
        "facts_years": {
            "min": min(fact["year"] for fact in historic_facts.values()),
            "max": max(fact["year"] for fact in historic_facts.values()),
            "all": sorted(set(fact["year"] for fact in historic_facts.values())),
        },
        "rulers_by_dynasty": dynasties_count,
        "oldest_fact": {
            "title": oldest_fact["title"] if oldest_fact else None,
            "year": oldest_fact["year"] if oldest_fact else None,
        },
        "newest_fact": {
            "title": newest_fact["title"] if newest_fact else None,
            "year": newest_fact["year"] if newest_fact else None,
        },
        "oldest_ruler": {
            "name": oldest_ruler["name"] if oldest_ruler else None,
            "start_year": get_start_year(oldest_ruler) if oldest_ruler else None,
        },
        "newest_ruler": {
            "name": newest_ruler["name"] if newest_ruler else None,
            "start_year": get_start_year(newest_ruler) if newest_ruler else None,
        },
    }

    logger.info("Запрос статистики")
    return stats
