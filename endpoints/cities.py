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
    },
    "11": {
        "name": "Санкт-Петербург",
        "country": "Россия",
        "population": 5600000,
        "founded": 1703,
        "fact": "Северная столица России, город белых ночей и разводных мостов. В центре города более 800 мостов.",
        "img_url": "https://avatars.mds.yandex.net/i?id=4a91f32feb632b2a6422b964b01d4037ae4e3e45-10812837-images-thumbs&n=13"
    },
    "12": {
        "name": "Казань",
        "country": "Россия",
        "population": 1300000,
        "founded": 1005,
        "fact": "Казань называют 'третьей столицей России'. Здесь официально зарегистрировано 115 национальностей.",
        "img_url": "https://avatars.mds.yandex.net/i?id=d042ebd6a465dcff1b964418bafd576019f4c540-5233966-images-thumbs&n=13"
    },
    "13": {
        "name": "Сочи",
        "country": "Россия",
        "population": 444000,
        "founded": 1838,
        "fact": "Самый длинный город Европы - протянулся вдоль побережья на 147 километров.",
        "img_url": "https://avatars.mds.yandex.net/i?id=e261aa3e3543fb54bddd1bcbc26862f4a62c84f7-9123854-images-thumbs&n=13"
    },
    "14": {
        "name": "Марсель",
        "country": "Франция",
        "population": 870000,
        "founded": 600,
        "fact": "Самый старый город Франции, основанный греками около 600 года до н.э. Знаменит своим супом буйабес.",
        "img_url": "https://avatars.mds.yandex.net/i?id=186554894378c3b155b3b60b5c71ca44952d2031-4958364-images-thumbs&n=13"
    },
    "15": {
        "name": "Лион",
        "country": "Франция",
        "population": 520000,
        "founded": 43,
        "fact": "Мировая столица гастрономии. Здесь родились братья Люмьер - создатели кинематографа.",
        "img_url": "https://avatars.mds.yandex.net/i?id=e7b4812bcdbcad0c3a2331398bb61c49005fa2a3-5232129-images-thumbs&n=13"
    },
    "16": {
        "name": "Александрия",
        "country": "Египет",
        "population": 5300000,
        "founded": 331,
        "fact": "В древности здесь находился знаменитый Александрийский маяк - одно из семи чудес света.",
        "img_url": "https://avatars.mds.yandex.net/i?id=2aa620caadcdc9ed694530173216bc68cc083791-8497835-images-thumbs&n=13"
    },
    "17": {
        "name": "Луксор",
        "country": "Египет",
        "population": 506000,
        "founded": -1400,
        "fact": "Город живых и город мёртвых. Здесь находятся знаменитые Карнакский и Луксорский храмы, а также Долина царей.",
        "img_url": "https://avatars.mds.yandex.net/i?id=20fb1cd5ddc101f281df802e1811e293c1d0bcc8-5520851-images-thumbs&n=13"
    },
    "18": {
        "name": "Венеция",
        "country": "Италия",
        "population": 260000,
        "founded": 421,
        "fact": "Город на воде состоит из 118 островов, соединённых 400 мостами. Здесь совсем нет автомобилей.",
        "img_url": "https://avatars.mds.yandex.net/i?id=501ddf3d85f4ebd76540e92385b01185fc1c9f43-3612431-images-thumbs&n=13"
    },
    "19": {
        "name": "Флоренция",
        "country": "Италия",
        "population": 382000,
        "founded": 59,
        "fact": "Колыбель эпохи Возрождения. Здесь творили Леонардо да Винчи, Микеланджело и Данте.",
        "img_url": "https://avatars.mds.yandex.net/i?id=931e79f9879377fc13f778308cb506ccc1447f14-5576459-images-thumbs&n=13"
    },
    "20": {
        "name": "Неаполь",
        "country": "Италия",
        "population": 960000,
        "founded": 750,
        "fact": "Родина пиццы. Именно здесь придумали знаменитую пиццу 'Маргарита'.",
        "img_url": "https://avatars.mds.yandex.net/i?id=7f69467c0966ddd58461c077bb0ce2c3613fe88a-4077354-images-thumbs&n=13"
    },
    "21": {
        "name": "Лос-Анджелес",
        "country": "США",
        "population": 3800000,
        "founded": 1781,
        "fact": "Мировая столица развлечений. Здесь находится Голливуд и снимается большинство фильмов.",
        "img_url": "https://avatars.mds.yandex.net/i?id=524875c29bbddb577df6d841ca53717a6b740f8e-4328379-images-thumbs&n=13"
    },
    "22": {
        "name": "Чикаго",
        "country": "США",
        "population": 2700000,
        "founded": 1833,
        "fact": "Город небоскрёбов - именно здесь построили первый в мире небоскрёб в 1885 году.",
        "img_url": "https://avatars.mds.yandex.net/i?id=50692526d93f7dcee9ca4b7766e0700935882ca4-10636899-images-thumbs&n=13"
    },
    "23": {
        "name": "Лас-Вегас",
        "country": "США",
        "population": 650000,
        "founded": 1905,
        "fact": "Город огней и казино в пустыне Мохаве. Ночью его видно из космоса как самое яркое пятно.",
        "img_url": "https://avatars.mds.yandex.net/i?id=3ef3206f47af2a262d799bc0219dc7ee531f8094-13290024-images-thumbs&n=13"
    },
    "24": {
        "name": "Шанхай",
        "country": "Китай",
        "population": 24870000,
        "founded": 1291,
        "fact": "Самый большой город Китая с самым быстрым поездом в мире - магнитопланом (430 км/ч).",
        "img_url": "https://avatars.mds.yandex.net/i?id=2257e76a0ba1681c24094ee34b9980f870fc0e43-5331218-images-thumbs&n=13"
    },
    "25": {
        "name": "Гонконг",
        "country": "Китай",
        "population": 7500000,
        "founded": 1842,
        "fact": "Город-государство с самым большим количеством небоскрёбов в мире - их больше 8000.",
        "img_url": "https://avatars.mds.yandex.net/i?id=79f9ce26c93959c4cce5ad28f285eddef78e9dac-8342484-images-thumbs&n=13"
    },
    "26": {
        "name": "Мумбаи",
        "country": "Индия",
        "population": 20400000,
        "founded": 1507,
        "fact": "Самый густонаселённый город Индии. Здесь находится Болливуд - индийская кинофабрика.",
        "img_url": "https://avatars.mds.yandex.net/i?id=2c68302bf706b1f322060011265a52cebd81bc64-5906238-images-thumbs&n=13"
    },
    "27": {
        "name": "Дели",
        "country": "Индия",
        "population": 32000000,
        "founded": -300,
        "fact": "Город, который разрушали и перестраивали 7 раз. Здесь смешались древность и современность.",
        "img_url": "https://avatars.mds.yandex.net/i?id=fb88f846c892f7c93109667403216add4f5170f4-9216096-images-thumbs&n=13"
    },
    "28": {
        "name": "Сан-Паулу",
        "country": "Бразилия",
        "population": 12300000,
        "founded": 1554,
        "fact": "Крупнейший город Южного полушария. Здесь вертолёты используют как такси - более 400 вертолётных площадок.",
        "img_url": "https://avatars.mds.yandex.net/i?id=5a625a3ae6c2054e65925dee50169326-5682746-images-thumbs&n=13"
    },
    "29": {
        "name": "Мельбурн",
        "country": "Австралия",
        "population": 5000000,
        "founded": 1835,
        "fact": "Самый европейский город Австралии. 7 лет подряд признавался самым комфортным городом мира.",
        "img_url": "https://avatars.mds.yandex.net/i?id=a6c4a233d154f01538fa7c8918a1d9da9ac02347-4101447-images-thumbs&n=13"
    },
    "30": {
        "name": "Осака",
        "country": "Япония",
        "population": 2690000,
        "founded": 645,
        "fact": "Город еды и кулинарная столица Японии. Здесь придумали знаменитое блюдо 'такояки'.",
        "img_url": "https://avatars.mds.yandex.net/i?id=02ada36536e3940a2be160d10872725e39c2631b-16330017-images-thumbs&n=13"
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
    },
    "13": {
        "name": "Эрмитаж",
        "city": "Санкт-Петербург",
        "country": "Россия",
        "type": "Музей",
        "year": 1764,
        "fact": "Эрмитаж - один из крупнейших музеев мира. Чтобы осмотреть все экспонаты, потратив на каждый по минуте, понадобится 11 лет",
        "img_url": "https://avatars.mds.yandex.net/i?id=673760c6c2186a2244983180b9ecdc8baf2033fd-8497195-images-thumbs&n=13"
    },
    "14": {
        "name": "Петропавловская крепость",
        "city": "Санкт-Петербург",
        "country": "Россия",
        "type": "Крепость",
        "year": 1703,
        "fact": "Именно с закладки этой крепости началось строительство Санкт-Петербурга. Здесь находится усыпальница российских императоров",
        "img_url": "https://avatars.mds.yandex.net/i?id=6ec090e6a97ba672932180d0ae74120cd3aa7d12-10245035-images-thumbs&n=13"
    },
    "15": {
        "name": "Исаакиевский собор",
        "city": "Санкт-Петербург",
        "country": "Россия",
        "type": "Собор",
        "year": 1858,
        "fact": "На строительство собора ушло 40 лет, а его колонны весят по 114 тонн каждая",
        "img_url": "https://culture.ru/_next/image?url=https%3A%2F%2Fwww.culture.ru%2Fstorage%2Fimages%2Fa08b8a52-6c53-543c-8fad-bfad83fe7ccb%2Fc_fill%2Cg_center%2F20210323_142649.jpg&w=1024&q=75"
    },
    
    # Казань (3 достопримечательности)
    "16": {
        "name": "Казанский Кремль",
        "city": "Казань",
        "country": "Россия",
        "type": "Крепость",
        "year": 1552,
        "fact": "Единственная в России крепость, где православный храм и мечеть находятся рядом и мирно соседствуют",
        "img_url": "https://avatars.mds.yandex.net/i?id=86c4bdfc3d2abca0bbc63b5a9236e1fa560fa66e-4079989-images-thumbs&n=13"
    },
    "17": {
        "name": "Мечеть Кул-Шариф",
        "city": "Казань",
        "country": "Россия",
        "type": "Мечеть",
        "year": 2005,
        "fact": "Главная мечеть Татарстана, восстановленная в память о древней мечети, разрушенной в 1552 году",
        "img_url": "https://avatars.mds.yandex.net/i?id=0905ed6f60650fbe497b89a1db1294744350d76c-9083123-images-thumbs&n=13"
    },
    "18": {
        "name": "Башня Сююмбике",
        "city": "Казань",
        "country": "Россия",
        "type": "Башня",
        "year": 1645,
        "fact": "Падающая башня Казани - отклонение от вертикали составляет почти 2 метра",
        "img_url": "https://upload.wikimedia.org/wikipedia/commons/5/57/Башня_Сююмбике_%28Республика_Татарстан%2C_Казань%2C_Кремль%29.JPG"
    },
    
    # Сочи (3 достопримечательности)
    "19": {
        "name": "Олимпийский парк",
        "city": "Сочи",
        "country": "Россия",
        "type": "Спортивный комплекс",
        "year": 2014,
        "fact": "Построен к зимней Олимпиаде 2014 года. Здесь проходили церемонии открытия и закрытия Игр",
        "img_url": "https://avatars.mds.yandex.net/i?id=df41237e2903e63ca6a2821407dc3041948821d0bf76d9b8-11431503-images-thumbs&n=13"
    },
    "20": {
        "name": "Роза Хутор",
        "city": "Сочи",
        "country": "Россия",
        "type": "Горнолыжный курорт",
        "year": 2010,
        "fact": "Горнолыжный курорт, где проходили соревнования зимних Олимпийских игр 2014 года",
        "img_url": "https://avatars.mds.yandex.net/i?id=b5eff6fa752344f9740121099a67c2304cbbe1ba-8899294-images-thumbs&n=13"
    },
    "21": {
        "name": "Дендрарий",
        "city": "Сочи",
        "country": "Россия",
        "type": "Парк",
        "year": 1892,
        "fact": "Уникальный парк с растениями со всего мира. Здесь растут секвойи высотой с 20-этажный дом",
        "img_url": "https://avatars.mds.yandex.net/i?id=1d7b20c14ea64ef77aa3e5e488f4b43780af1245-10160311-images-thumbs&n=13"
    },
    
    # Марсель (Франция)
    "22": {
        "name": "Базилика Нотр-Дам-де-ла-Гард",
        "city": "Марсель",
        "country": "Франция",
        "type": "Собор",
        "year": 1864,
        "fact": "Главный символ Марселя, возвышающийся над городом. Местные жители называют её 'Хорошая мать'",
        "img_url": "https://avatars.mds.yandex.net/i?id=012427976425f87ea276dc786c85096dfc92cf40-8999179-images-thumbs&n=13"
    },
    
    # Лион (Франция)
    "23": {
        "name": "Базилика Нотр-Дам-де-Фурвьер",
        "city": "Лион",
        "country": "Франция",
        "type": "Собор",
        "year": 1896,
        "fact": "С холма Фурвьер открывается лучший вид на Лион. Считается, что именно здесь христианство пришло в Галлию",
        "img_url": "https://avatars.mds.yandex.net/i?id=46e3480f0f922a45324facb9c57aa3ccb40ec23c-3006415-images-thumbs&n=13"
    },
    
    # Александрия (Египет)
    "24": {
        "name": "Библиотека Александрина",
        "city": "Александрия",
        "country": "Египет",
        "type": "Библиотека",
        "year": 2002,
        "fact": "Современная библиотека построена на месте знаменитой Александрийской библиотеки древности. В ней 8 миллионов книг",
        "img_url": "https://avatars.mds.yandex.net/i?id=b940450b7874fb00fce20b38add64b340fe63cf6-5367334-images-thumbs&n=13"
    },
    
    # Луксор (Египет)
    "25": {
        "name": "Карнакский храм",
        "city": "Луксор",
        "country": "Египет",
        "type": "Древний храм",
        "year": -1600,
        "fact": "Крупнейший храмовый комплекс Древнего Египта. Его зал с колоннами мог бы вместить парижский собор Нотр-Дам",
        "img_url": "https://avatars.mds.yandex.net/i?id=2b90aeeedc1cbfb795835aa61380df782320b07a-10197150-images-thumbs&n=13"
    },
    
    # Венеция (Италия)
    "26": {
        "name": "Собор Святого Марка",
        "city": "Венеция",
        "country": "Италия",
        "type": "Собор",
        "year": 1092,
        "fact": "Собор украшен 4000 квадратными метрами золотой мозаики, за что получил прозвище 'Золотая базилика'",
        "img_url": "https://avatars.mds.yandex.net/i?id=207d6ad6b8bbd73ac81d002ccffbd7b291198353-5382665-images-thumbs&n=13"
    },
    
    # Флоренция (Италия)
    "27": {
        "name": "Собор Санта-Мария-дель-Фьоре",
        "city": "Флоренция",
        "country": "Италия",
        "type": "Собор",
        "year": 1436,
        "fact": "Его купол - шедевр архитектуры, построенный без поддерживающих лесов. До сих пор крупнейший кирпичный купол в мире",
        "img_url": "https://avatars.mds.yandex.net/i?id=2a6d5bfd31df54986d40f9159d7a9bc3cf674df7-10499278-images-thumbs&n=13"
    },
    
    # Неаполь (Италия)
    "28": {
        "name": "Помпеи",
        "city": "Неаполь",
        "country": "Италия",
        "type": "Археологический комплекс",
        "year": -600,
        "fact": "Город, погибший при извержении Везувия в 79 году н.э. Раскопки продолжаются до сих пор",
        "img_url": "https://avatars.mds.yandex.net/i?id=2692e8305567ee56249dd5570f3f92c1-4010157-images-thumbs&n=13"
    },
    
    # Лос-Анджелес (США)
    "29": {
        "name": "Голливуд",
        "city": "Лос-Анджелес",
        "country": "США",
        "type": "Район",
        "year": 1910,
        "fact": "Знаменитая надпись HOLLYWOOD первоначально была HOLLYWOODLAND и рекламировала новый жилой комплекс",
        "img_url": "https://avatars.mds.yandex.net/i?id=8f0cf11d4a64b3af6cfe7612a8b9f31d241c550b-10157623-images-thumbs&n=13"
    },
    
    # Чикаго (США)
    "30": {
        "name": "Уиллис-тауэр",
        "city": "Чикаго",
        "country": "США",
        "type": "Небоскрёб",
        "year": 1973,
        "fact": "Стеклянные балконы на 103 этаже выступают на 1.2 метра из здания на высоте 412 метров",
        "img_url": "https://avatars.mds.yandex.net/i?id=bdafb24efb99ac28a1151ae09df6b07c997ab691-12371687-images-thumbs&n=13"
    },
    
    # Лас-Вегас (США)
    "31": {
        "name": "Лас-Вегас-Стрип",
        "city": "Лас-Вегас",
        "country": "США",
        "type": "Улица",
        "year": 1931,
        "fact": "7-километровый отрезок бульвара с самыми известными казино и отелями. Ночью здесь включается 15 миллионов лампочек",
        "img_url": "https://avatars.mds.yandex.net/i?id=ab55392dc7467faa819043add96fda40bfaddb32-12714644-images-thumbs&n=13"
    },
    
    # Шанхай (Китай)
    "32": {
        "name": "Башня Шанхай",
        "city": "Шанхай",
        "country": "Китай",
        "type": "Небоскрёб",
        "year": 2015,
        "fact": "Третье по высоте здание в мире (632 метра). У него самый быстрый лифт - поднимается со скоростью 20.5 м/с",
        "img_url": "https://avatars.mds.yandex.net/i?id=e5852c10bc989c573e28f2c25e9bdc4e77f711c1-12421254-images-thumbs&n=13"
    },
    
    # Гонконг (Китай)
    "33": {
        "name": "Пик Виктория",
        "city": "Гонконг",
        "country": "Китай",
        "type": "Гора",
        "year": 1888,
        "fact": "Самая высокая точка Гонконга. На вершину ведёт старейший фуникулёр Азии",
        "img_url": "https://avatars.mds.yandex.net/i?id=08a7f2f4f2912bcd5b267b074e2f62d16545158b-5323298-images-thumbs&n=13"
    },
    
    # Мумбаи (Индия)
    "34": {
        "name": "Ворота Индии",
        "city": "Мумбаи",
        "country": "Индия",
        "type": "Памятник",
        "year": 1924,
        "fact": "Триумфальная арка построена в честь визита короля Георга V. Через неё уходили последние британские солдаты",
        "img_url": "https://avatars.mds.yandex.net/i?id=8befcc64406e35c1b3565dc112e9f19bef14dd35-8411463-images-thumbs&n=13"
    },
    
    # Дели (Индия)
    "35": {
        "name": "Кутб-Минар",
        "city": "Дели",
        "country": "Индия",
        "type": "Башня",
        "year": 1193,
        "fact": "Самая высокая кирпичная башня в мире (73 метра). Рядом стоит знаменитая Железная колонна, которая не ржавеет 1600 лет",
        "img_url": "https://avatars.mds.yandex.net/i?id=405484d81dad4d4e27f2ba5aecdff2d81a789e7b-12775993-images-thumbs&n=13"
    },
    
    # Сан-Паулу (Бразилия)
    "36": {
        "name": "Музей искусства Сан-Паулу",
        "city": "Сан-Паулу",
        "country": "Бразилия",
        "type": "Музей",
        "year": 1968,
        "fact": "Здание висит на двух красных порталах над землёй. Под ним проходит оживлённая улица",
        "img_url": "https://avatars.mds.yandex.net/i?id=b06da181f15d6e444665a3b07b542a1df1a72727-5843214-images-thumbs&n=13"
    },
    
    # Мельбурн (Австралия)
    "37": {
        "name": "Мельбурн Крикет Граунд",
        "city": "Мельбурн",
        "country": "Австралия",
        "type": "Стадион",
        "year": 1853,
        "fact": "Огромный стадион вмещает 100000 зрителей. Во время Олимпиады 1956 года здесь проходили соревнования",
        "img_url": "https://avatars.mds.yandex.net/i?id=113e2c5bf22a1e1638689b13354d5175d9a3a927-4592676-images-thumbs&n=13"
    },
    
    # Осака (Япония)
    "38": {
        "name": "Замок Осака",
        "city": "Осака",
        "country": "Япония",
        "type": "Замок",
        "year": 1583,
        "fact": "Один из самых знаменитых замков Японии. Его главная башня украшена золотом и сияет на солнце",
        "img_url": "https://avatars.mds.yandex.net/i?id=9e4b9ea23907702ee8e7241e80556ec7a82c8c74-7000115-images-thumbs&n=13"
    },
    
    # Дополнительные для уже существующих городов (чтобы было по 3 в крупных)
    "39": {
        "name": "Третьяковская галерея",
        "city": "Москва",
        "country": "Россия",
        "type": "Музей",
        "year": 1856,
        "fact": "Главный музей русского искусства. Здесь собрано более 180 тысяч произведений искусства",
        "img_url": "https://avatars.mds.yandex.net/i?id=cbc5015a72580b0d490ffb361265761417e88a6e-4055806-images-thumbs&n=13"
    },
    "40": {
        "name": "Храм Василия Блаженного",
        "city": "Москва",
        "country": "Россия",
        "type": "Собор",
        "year": 1561,
        "fact": "Собор состоит из 9 церквей на одном фундаменте. По легенде, Ивану Грозному так понравился собор, что он приказал ослепить архитектора",
        "img_url": "https://avatars.mds.yandex.net/i?id=7f76b25201a9974fbe982827bbbca2c707f05459-5283550-images-thumbs&n=13"
    },
    "41": {
        "name": "Версаль",
        "city": "Париж",
        "country": "Франция",
        "type": "Дворец",
        "year": 1682,
        "fact": "В Версале 2300 комнат, 67 лестниц и 521 зеркало. Здесь был подписан Версальский договор",
        "img_url": "https://avatars.mds.yandex.net/i?id=614627caa1a6e54e41382804dc861cf3abff4e2e-5321688-images-thumbs&n=13"
    },
    "42": {
        "name": "Ватикан",
        "city": "Рим",
        "country": "Италия",
        "type": "Государство",
        "year": 1929,
        "fact": "Самое маленькое государство в мире (0.44 км²). Здесь находится собор Святого Петра и Сикстинская капелла",
        "img_url": "https://avatars.mds.yandex.net/i?id=a368e9cbb51668ef5e9b7bde308e01897a5b8f40-5233398-images-thumbs&n=13"
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