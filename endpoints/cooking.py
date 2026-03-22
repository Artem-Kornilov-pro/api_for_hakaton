from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import random
from typing import Optional, List

# Настройка логирования
logger = logging.getLogger(__name__)

cooking_router = APIRouter(tags=["cooking"])

# О великих поварах
chefs = {
    "1": {
        "name": "Константин Ивлев",
        "birth_year": 1974,
        "country": "Россия",
        "specialization": "Новая Русская Кухня",
        "text": """Константин Витальевич Ивлев — российский шеф-повар, бизнесмен, ресторатор, телеведущий, видеоблогер и автор книг по кулинарии. Основатель кулинарного направления «Новая Русская Кухня», управляющей компании Ivlev Group и брендов Ivlev Chef Production, а также Ivlev Chef BY Home Kitchen. 
Родился 12 января 1974 года в Москве. После окончания школы учился в ПТУ №19 по специальности «повар». 
Начал работать в ресторанной индустрии с 1993 года. Несколько лет работал поваром-универсалом, а затем и су-шефом в столичных кафе и ресторанах: «Стейк-Хаус», «Диана», «Ностальжи». Также проходил профессиональные стажировки в зарубежных ресторанах, обучался и работал под началом знаменитого «мишленовского» кулинара Патрика Пажеса""",
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/5674964/1247603642/SUx182_2x",
        "restaurants": ["The Сад", "Dr. Живаго", "Вареничная №1"],
        "tv_shows": ["Адская кухня", "На ножах", "Битва шефов"],
    },
    "2": {
        "name": "Алена Солодовиченко",
        "birth_year": 1988,
        "country": "Россия",
        "specialization": "Авторская кухня",
        "text": """Алена Солодовиченко — российский шеф-повар, телеведущая и ресторатор. Известна своей работой в ресторане «Selfie» и участием в телепроекте «Адская кухня». Специализируется на современной авторской кухне с элементами русских традиций. 
Родилась в 1988 году. Начала кулинарную карьеру с работы в ресторане «Галерея» под руководством Александра Раппопорта. Проходила стажировки в Европе. В 2016 году стала шеф-поваром ресторана Selfie, который получил признание критиков и вошел в список лучших ресторанов Москвы.""",
        "img_url": "https://avatars.mds.yandex.net/i?id=cd6c86266d06a58ac87d6c401123fef0147b7dce-4402429-images-thumbs&n=13",
        "restaurants": ["Selfie"],
        "tv_shows": ["Адская кухня", "ПроСТО кухня"],
    },
    "3": {
        "name": "Владимир Мухин",
        "birth_year": 1988,
        "country": "Россия",
        "specialization": "Современная русская кухня",
        "text": """Владимир Мухин — российский шеф-повар, ресторатор. Шеф-повар ресторана White Rabbit, который неоднократно входил в список 50 лучших ресторанов мира. Активно занимается популяризацией современной русской кухни и переосмыслением традиционных рецептов.
Родился в семье поваров в Краснодаре. Работал в ресторанах Москвы, проходил стажировки в лучших ресторанах мира. В 2019 году получил премию «Шеф-повар года» по версии GQ. White Rabbit под его руководством несколько лет подряд занимал место в топ-50 лучших ресторанов мира.""",
        "img_url": "https://avatars.mds.yandex.net/i?id=dc032869f5ab38c3d036f6d426853f0b66b7a421-12938156-images-thumbs&n=13",
        "restaurants": ["White Rabbit", "Сыроварня"],
        "tv_shows": ["На ножах", "Моя-твоя еда"],
    },
    "4": {
        "name": "Гордон Рамзи",
        "birth_year": 1966,
        "country": "Великобритания",
        "specialization": "Европейская кухня",
        "text": """Гордон Рамзи — британский шеф-повар, ресторатор и телеведущий. Обладатель 16 звезд Мишлен. Известен своим вспыльчивым характером на телешоу и исключительным профессионализмом в кулинарии.
Родился в Шотландии. Изучал кулинарию под руководством знаменитых шеф-поваров в Лондоне и Париже. Владеет сетью ресторанов по всему миру. Написал множество кулинарных книг. Стал знаменитым благодаря телешоу «Адская кухня», «Кошмары на кухне» и «МастерШеф».""",
        "img_url": "https://avatars.mds.yandex.net/i?id=8c774e92636ffceca1756dc47179de0d8c7856d4-4499319-images-thumbs&n=13",
        "restaurants": ["Restaurant Gordon Ramsay", "Bread Street Kitchen"],
        "tv_shows": ["Hell's Kitchen", "MasterChef", "Kitchen Nightmares"],
    },
    "5": {
        "name": "Екатерина Алехина",
        "birth_year": 1984,
        "country": "Россия",
        "specialization": "Высокая кухня",
        "text": """Екатерина Алехина — российский шеф-повар, первая россиянка, получившая звезду Мишлен. Шеф-повар ресторана Artest в Москве. Известна своим филигранным подходом к приготовлению блюд и использованием локальных продуктов.
Начала карьеру в ресторанном бизнесе с должности официантки, затем училась кулинарному искусству в Италии и Франции. Работала в ресторанах Москвы и Европы. В 2019 году возглавила ресторан Artest, который в 2021 году получил звезду Мишлен — первую в истории российских ресторанов.""",
        "img_url": "https://avatars.mds.yandex.net/i?id=993e8f60e630593b4925de3a792047b3f9e4ebb8-4238238-images-thumbs&n=13",
        "restaurants": ["Artest"],
        "tv_shows": ["МастерШеф"],
    },
}

# О блюдах
dishes = {
    "1": {
        "name": "Борщ",
        "country": "Россия/Украина",
        "type": "Суп",
        "description": "Традиционный восточноевропейский суп из свеклы, который придает ему характерный красный цвет. Готовится с мясом, капустой, картофелем, морковью и луком. Подается со сметаной и зеленью.",
        "ingredients": [
            "свекла",
            "капуста",
            "картофель",
            "мясо",
            "морковь",
            "лук",
            "томатная паста",
        ],
        "calories": 120,
        "cooking_time_minutes": 120,
        "img_url": "https://avatars.mds.yandex.net/i?id=c7e0f5e860966cdef65cd58f93382493fdabc339-12473708-images-thumbs&n=13",
    },
    "2": {
        "name": "Оливье",
        "country": "Россия",
        "type": "Салат",
        "description": "Популярный в странах бывшего СССР салат, названный в честь французского повара Люсьена Оливье. Готовится из отварных овощей, яиц, колбасы или мяса, заправляется майонезом.",
        "ingredients": [
            "картофель",
            "морковь",
            "яйца",
            "колбаса",
            "огурцы соленые",
            "горошек",
            "майонез",
        ],
        "calories": 250,
        "cooking_time_minutes": 60,
        "img_url": "https://avatars.mds.yandex.net/i?id=178a703916e6b151b0520a231bc0787cbfb8fd22-5283209-images-thumbs&n=13",
    },
    "3": {
        "name": "Пельмени",
        "country": "Россия",
        "type": "Основное блюдо",
        "description": "Блюдо из пресного теста с мясной начинкой. Традиционно подаются с маслом, сметаной или уксусом. Существует множество региональных вариаций.",
        "ingredients": ["мука", "яйца", "свинина", "говядина", "лук", "соль", "перец"],
        "calories": 275,
        "cooking_time_minutes": 45,
        "img_url": "https://avatars.mds.yandex.net/i?id=4b10394e44987a7a072eaa5f495fafe19429add2-3674583-images-thumbs&n=13",
    },
    "4": {
        "name": "Блины",
        "country": "Россия",
        "type": "Выпечка",
        "description": "Традиционное русское блюдо из жидкого теста, выпекаемое на сковороде. Подаются с различными начинками: икрой, рыбой, грибами, творогом, вареньем или сметаной.",
        "ingredients": ["мука", "молоко", "яйца", "сахар", "соль", "масло"],
        "calories": 150,
        "cooking_time_minutes": 30,
        "img_url": "https://avatars.mds.yandex.net/i?id=6754c1c00e734d5b91ba3aa1d33a50bbc1a15353-4842027-images-thumbs&n=13",
    },
    "5": {
        "name": "Щи",
        "country": "Россия",
        "type": "Суп",
        "description": "Традиционный русский суп из квашеной или свежей капусты. Существует множество вариаций: постные щи, щи с мясом, суточные щи, зеленые щи из щавеля.",
        "ingredients": ["капуста", "мясо", "картофель", "морковь", "лук", "томаты", "зелень"],
        "calories": 90,
        "cooking_time_minutes": 90,
        "img_url": "https://avatars.mds.yandex.net/i?id=acec9633762afc07b4365d782a9315ed0defb34a-13124761-images-thumbs&n=13",
    },
    "6": {
        "name": "Уха",
        "country": "Россия",
        "type": "Суп",
        "description": "Традиционный русский рыбный суп. Готовится из разных видов рыбы, с добавлением картофеля, моркови и лука. Особенность ухи — прозрачный наваристый бульон.",
        "ingredients": ["рыба", "картофель", "морковь", "лук", "лавровый лист", "перец", "зелень"],
        "calories": 70,
        "cooking_time_minutes": 60,
        "img_url": "https://avatars.mds.yandex.net/i?id=8e3bf5fdafab061a0eab45da1cf56da0bc9da52b-12540153-images-thumbs&n=13",
    },
    "7": {
        "name": "Бефстроганов",
        "country": "Россия",
        "type": "Основное блюдо",
        "description": "Популярное блюдо русской кухни из мелко нарезанной говядины, залитой горячим сметанным соусом. Названо в честь графа Строганова.",
        "ingredients": ["говядина", "лук", "сметана", "мука", "томатная паста", "грибы", "масло"],
        "calories": 220,
        "cooking_time_minutes": 50,
        "img_url": "https://avatars.mds.yandex.net/i?id=83e847576cc95407498d3f648c77492a6fa10c9f-10576628-images-thumbs&n=13",
    },
    "8": {
        "name": "Котлета по-киевски",
        "country": "Украина/Россия",
        "type": "Основное блюдо",
        "description": "Куриная котлета, в которую завернут кусочек холодного сливочного масла с зеленью. При жарке масло растапливается, делая котлету сочной внутри с хрустящей корочкой снаружи.",
        "ingredients": ["куриное филе", "масло сливочное", "зелень", "яйца", "сухари панировочные"],
        "calories": 320,
        "cooking_time_minutes": 40,
        "img_url": "https://avatars.mds.yandex.net/i?id=553eff59facdc8ca6f044107896a948e188611db-4389782-images-thumbs&n=13",
    },
    "9": {
        "name": "Пирожки",
        "country": "Россия",
        "type": "Выпечка",
        "description": "Небольшие изделия из дрожжевого теста с различными начинками. Могут быть печеными или жареными. Популярны как самостоятельное блюдо или дополнение к супам.",
        "ingredients": [
            "мука",
            "дрожжи",
            "молоко",
            "яйца",
            "сахар",
            "начинка (капуста, мясо, картошка, яблоки)",
        ],
        "calories": 280,
        "cooking_time_minutes": 120,
        "img_url": "https://avatars.mds.yandex.net/i?id=b9caf133b2dd4ffbe8513ba590e3aff652494ddd-11375516-images-thumbs&n=13",
    },
    "10": {
        "name": "Квас",
        "country": "Россия",
        "type": "Напиток",
        "description": "Традиционный славянский кисловатый напиток, который готовят путем брожения из ржаного хлеба, солода и сахара. Освежающий напиток, особенно популярный летом.",
        "ingredients": ["хлеб ржаной", "сахар", "дрожжи", "вода", "изюм"],
        "calories": 40,
        "cooking_time_minutes": 2880,
        "img_url": "https://avatars.mds.yandex.net/i?id=d8296790addbe75a7c8ce2f0f84a839672b2ba6f-17806471-images-thumbs&n=13",
    },
    "11": {
        "name": "Пицца Маргарита",
        "country": "Италия",
        "type": "Основное блюдо",
        "description": "Классическая итальянская пицца с томатным соусом, сыром моцарелла и свежим базиликом. Названа в честь королевы Маргариты Савойской, а её цвета повторяют итальянский флаг.",
        "ingredients": [
            "тесто для пиццы",
            "томатный соус",
            "моцарелла",
            "базилик",
            "оливковое масло",
            "соль",
        ],
        "calories": 250,
        "cooking_time_minutes": 20,
        "img_url": "https://avatars.mds.yandex.net/i?id=abb43a4bcbcef3ddb50f9cf842ac46d2dff77af6-5193708-images-thumbs&n=13",
    },
    "12": {
        "name": "Лазанья",
        "country": "Италия",
        "type": "Основное блюдо",
        "description": "Традиционное итальянское блюдо из слоёв пасты, мясного соуса болоньезе, соуса бешамель и сыра пармезан. Запекается в духовке до золотистой корочки.",
        "ingredients": [
            "листы лазаньи",
            "фарш мясной",
            "томаты",
            "лук",
            "морковь",
            "соус бешамель",
            "пармезан",
        ],
        "calories": 350,
        "cooking_time_minutes": 60,
        "img_url": "https://avatars.mds.yandex.net/i?id=fd79ca0d2a5be00f416cc05006d1f01f1c1ea402-5747098-images-thumbs&n=13",
    },
    "13": {
        "name": "Ризотто",
        "country": "Италия",
        "type": "Основное блюдо",
        "description": "Кремовое блюдо из риса, которое готовят на бульоне с добавлением различных ингредиентов. Классический вариант - с грибами или шафраном.",
        "ingredients": [
            "рис арборио",
            "бульон",
            "лук",
            "белое вино",
            "пармезан",
            "сливочное масло",
            "грибы",
        ],
        "calories": 280,
        "cooking_time_minutes": 30,
        "img_url": "https://avatars.mds.yandex.net/i?id=76f120046ca7c107279f288b7aee24ff0e7b9c4f-3552885-images-thumbs&n=13",
    },
    "14": {
        "name": "Тирамису",
        "country": "Италия",
        "type": "Десерт",
        "description": "Знаменитый итальянский десерт из слоёв печенья савоярди, пропитанного кофе, и нежного крема из маскарпоне. Сверху посыпается какао-порошком.",
        "ingredients": [
            "маскарпоне",
            "печенье савоярди",
            "кофе эспрессо",
            "яйца",
            "сахар",
            "какао",
        ],
        "calories": 380,
        "cooking_time_minutes": 40,
        "img_url": "https://avatars.mds.yandex.net/i?id=98d96e5e711ce455bb1345c316a7580197931da4-12481555-images-thumbs&n=13",
    },
    "15": {
        "name": "Джелато",
        "country": "Италия",
        "type": "Десерт",
        "description": "Итальянское мороженое, которое отличается от обычного более плотной текстурой и насыщенным вкусом. В нём меньше жира и воздуха, чем в обычном мороженом.",
        "ingredients": ["молоко", "сливки", "сахар", "яичные желтки", "натуральные ароматизаторы"],
        "calories": 200,
        "cooking_time_minutes": 60,
        "img_url": "https://www.refro.ru/upload/medialibrary/efd/efdb5917cba6813b27353ca42d366c9a.jpg",
    },
    "16": {
        "name": "Круассан",
        "country": "Франция",
        "type": "Выпечка",
        "description": "Знаменитая французская выпечка из слоёного теста в форме полумесяца. Хрустящий снаружи и мягкий внутри, идеально подходит для завтрака с кофе.",
        "ingredients": ["мука", "сливочное масло", "молоко", "дрожжи", "сахар", "соль"],
        "calories": 300,
        "cooking_time_minutes": 180,
        "img_url": "https://avatars.mds.yandex.net/i?id=aa9bec6294fc618eee82d975a6a82e635ffdb53e-10766029-images-thumbs&n=13",
    },
    "17": {
        "name": "Луковый суп",
        "country": "Франция",
        "type": "Суп",
        "description": "Традиционный французский суп из карамелизированного лука на мясном бульоне. Подаётся с гренками, покрытыми расплавленным сыром.",
        "ingredients": [
            "лук репчатый",
            "говяжий бульон",
            "сыр грюйер",
            "багет",
            "сливочное масло",
            "тимьян",
        ],
        "calories": 180,
        "cooking_time_minutes": 60,
        "img_url": "https://avatars.mds.yandex.net/i?id=8ebd6c7e1737c7bc49a6efb099b1cdfa611424d8-5410274-images-thumbs&n=13",
    },
    "18": {
        "name": "Киш Лорен",
        "country": "Франция",
        "type": "Выпечка",
        "description": "Открытый пирог из песочного теста с начинкой из яиц, сливок, бекона и сыра. Одно из самых известных блюд французской кухни.",
        "ingredients": [
            "мука",
            "масло сливочное",
            "яйца",
            "сливки",
            "бекон",
            "сыр",
            "мускатный орех",
        ],
        "calories": 320,
        "cooking_time_minutes": 50,
        "img_url": "https://avatars.mds.yandex.net/i?id=d973da450198b3895216d8b6b16a589cdaada280-5436653-images-thumbs&n=13",
    },
    "19": {
        "name": "Конфи из утки",
        "country": "Франция",
        "type": "Основное блюдо",
        "description": "Традиционное блюдо из утиных ножек, медленно томлёных в собственном жире. Мясо получается невероятно нежным и ароматным.",
        "ingredients": [
            "утиные ножки",
            "утиный жир",
            "чеснок",
            "тимьян",
            "соль",
            "перец",
            "лавровый лист",
        ],
        "calories": 350,
        "cooking_time_minutes": 180,
        "img_url": "https://avatars.mds.yandex.net/i?id=ad9d3c3376890e558ccfa6a101e59553681bf60c-5877861-images-thumbs&n=13",
    },
    "20": {
        "name": "Макарон",
        "country": "Франция",
        "type": "Десерт",
        "description": "Изысканное французское пирожное из двух миндальных половинок, соединённых кремом. Бывает разных цветов и вкусов.",
        "ingredients": [
            "миндальная мука",
            "сахарная пудра",
            "яичные белки",
            "сахар",
            "сливочный крем",
        ],
        "calories": 120,
        "cooking_time_minutes": 90,
        "img_url": "https://avatars.mds.yandex.net/i?id=dd2d68e856181eafacf84887471cbc2188580538-5026463-images-thumbs&n=13",
    },
    # Мексиканская кухня (2 блюда)
    "21": {
        "name": "Тако",
        "country": "Мексика",
        "type": "Основное блюдо",
        "description": "Мексиканское блюдо из кукурузной или пшеничной лепёшки с начинкой из мяса, овощей, сыра и острого соуса. Подаётся с лаймом и свежей кинзой.",
        "ingredients": [
            "кукурузные лепёшки",
            "говядина",
            "лук",
            "кинза",
            "лайм",
            "острый соус",
            "сыр",
        ],
        "calories": 220,
        "cooking_time_minutes": 30,
        "img_url": "https://avatars.mds.yandex.net/i?id=a2c2f2c9eb0426ac267346b7ceac70210d882813-16921400-images-thumbs&n=13",
    },
    "22": {
        "name": "Гуакамоле",
        "country": "Мексика",
        "type": "Закуска",
        "description": "Традиционная мексиканская закуска из пюре авокадо с добавлением лука, помидоров, кинзы и сока лайма. Подаётся с кукурузными чипсами.",
        "ingredients": ["авокадо", "помидоры", "лук", "кинза", "лайм", "перец чили", "соль"],
        "calories": 150,
        "cooking_time_minutes": 15,
        "img_url": "https://cdnn21.img.ria.ru/images/07e9/02/06/1997826433_0:6:1344:762_1920x0_80_0_0_8a54b5384b3de3cb6ebe66b9ed8bab9f.jpg",
    },
    # Тайская кухня (2 блюда)
    "23": {
        "name": "Том Ям",
        "country": "Таиланд",
        "type": "Суп",
        "description": "Знаменитый тайский острый кислый суп на кокосовом молоке с креветками, грибами, лимонником и листьями лайма. Идеальный баланс пяти вкусов.",
        "ingredients": [
            "кокосовое молоко",
            "креветки",
            "грибы",
            "лемонграсс",
            "каффир-лайм",
            "чили",
            "рыбный соус",
        ],
        "calories": 180,
        "cooking_time_minutes": 40,
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2238866/1244016663/SUx182_2x",
    },
    "24": {
        "name": "Пад Тай",
        "country": "Таиланд",
        "type": "Основное блюдо",
        "description": "Тайская рисовая лапша быстрого приготовления с тофу, креветками, яйцом, ростками бобов и арахисом. Подаётся с лаймом и рыбным соусом.",
        "ingredients": [
            "рисовая лапша",
            "креветки",
            "тофу",
            "яйца",
            "ростки бобов",
            "арахис",
            "рыбный соус",
        ],
        "calories": 320,
        "cooking_time_minutes": 25,
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/2300207/1244956077/SUx182_2x",
    },
    # Греческая кухня (2 блюда)
    "25": {
        "name": "Греческий салат",
        "country": "Греция",
        "type": "Салат",
        "description": "Классический греческий салат из свежих овощей, оливок и сыра фета. Заправляется оливковым маслом и орегано. В Греции его называют 'хорьятики' - деревенский салат.",
        "ingredients": ["помидоры", "огурцы", "перец", "лук", "фета", "оливки", "оливковое масло"],
        "calories": 180,
        "cooking_time_minutes": 15,
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1554108/1237944627/S600xU_2x",
    },
    "26": {
        "name": "Муссака",
        "country": "Греция",
        "type": "Основное блюдо",
        "description": "Традиционная греческая запеканка из слоёв баклажанов, картофеля, мясного фарша и соуса бешамель. Запекается до золотистой корочки.",
        "ingredients": [
            "баклажаны",
            "картофель",
            "фарш бараний",
            "томаты",
            "лук",
            "соус бешамель",
            "сыр",
        ],
        "calories": 380,
        "cooking_time_minutes": 90,
        "img_url": "https://images.news.ru/2025/08/04/Qpzy6O4aHI0W5SdiFmXRVuhscXSx4J3Z2yWKINIl_780.png",
    },
    # Грузинская кухня (2 блюда)
    "27": {
        "name": "Хачапури",
        "country": "Грузия",
        "type": "Выпечка",
        "description": "Грузинский хлеб с сыром. Существует много видов: по-аджарски (лодочка с яйцом), по-имеретински (закрытая лепёшка) и другие. Национальная гордость Грузии.",
        "ingredients": ["мука", "сыр сулугуни", "мацони", "яйца", "масло", "дрожжи"],
        "calories": 290,
        "cooking_time_minutes": 45,
        "img_url": "https://avatars.mds.yandex.net/get-entity_search/1966007/1243913138/SUx182_2x",
    },
    "28": {
        "name": "Хинкали",
        "country": "Грузия",
        "type": "Основное блюдо",
        "description": "Грузинские пельмени с мясной начинкой и бульоном внутри. Едят руками, держа за хвостик из теста. Внутри обязательно должен оставаться горячий бульон.",
        "ingredients": ["мука", "говядина", "свинина", "лук", "чеснок", "кинза", "перец"],
        "calories": 250,
        "cooking_time_minutes": 50,
        "img_url": "https://avatars.mds.yandex.net/i?id=8aa21bda1c49ea187a0e7a6c20affa1656b4dcc7-10025673-images-thumbs&n=13",
    },
}


# Вспомогательная функция для проверки существования повара
def get_chef_or_404(chef_id: str):
    if chef_id not in chefs:
        raise HTTPException(status_code=404, detail=f"Повар с ID {chef_id} не найден")
    return chefs[chef_id]


# Вспомогательная функция для проверки существования блюда
def get_dish_or_404(dish_id: str):
    if dish_id not in dishes:
        raise HTTPException(status_code=404, detail=f"Блюдо с ID {dish_id} не найдено")
    return dishes[dish_id]


# ========== ЭНДПОИНТЫ ДЛЯ ПОВАРОВ ==========


# Простые эндпоинты
@cooking_router.get("/all_chef")
async def all_chef():
    """
    Простой эндпоинт: информация обо всех шеф-поварах
    """
    logger.info("Запрос всех поваров")
    return chefs


@cooking_router.get("/random_chef")
async def random_chef():
    """
    Простой эндпоинт: информация о случайном шеф-поваре
    """
    chef_id = random.choice(list(chefs.keys()))
    logger.info(f"Случайный повар с ID: {chef_id}")
    return chefs[chef_id]


# Сложные эндпоинты для поваров
@cooking_router.get("/chef/{chef_id}")
async def get_chef_by_id(chef_id: str):
    """
    Сложный эндпоинт: информация о конкретном поваре по ID
    """
    return get_chef_or_404(chef_id)


@cooking_router.get("/chef/born_after/{year}")
async def get_chefs_born_after(year: int):
    """
    Сложный эндпоинт: повара, родившиеся после указанного года
    """
    result = {chef_id: chef for chef_id, chef in chefs.items() if chef["birth_year"] > year}
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Повары, родившиеся после {year} года, не найдены"
        )
    logger.info(f"Запрос поваров, родившихся после {year}")
    return result


@cooking_router.get("/chef/by_restaurant/{restaurant}")
async def get_chefs_by_restaurant(restaurant: str):
    """
    Сложный эндпоинт: повара, работающие в указанном ресторане
    """
    result = {}
    for chef_id, chef in chefs.items():
        if any(restaurant.lower() in r.lower() for r in chef["restaurants"]):
            result[chef_id] = chef

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Повары, работающие в ресторане '{restaurant}', не найдены"
        )
    logger.info(f"Запрос поваров ресторана: {restaurant}")
    return result


# ========== ЭНДПОИНТЫ ДЛЯ БЛЮД ==========


# Простые эндпоинты
@cooking_router.get("/all_dishes")
async def all_dishes():
    """
    Простой эндпоинт: информация обо всех блюдах
    """
    logger.info("Запрос всех блюд")
    return dishes


@cooking_router.get("/random_dish")
async def random_dish():
    """
    Простой эндпоинт: информация о случайном блюде
    """
    dish_id = random.choice(list(dishes.keys()))
    logger.info(f"Случайное блюдо с ID: {dish_id}")
    return dishes[dish_id]


# Сложные эндпоинты для блюд
@cooking_router.get("/dish/{dish_id}")
async def get_dish_by_id(dish_id: str):
    """
    Сложный эндпоинт: информация о конкретном блюде по ID
    """
    return get_dish_or_404(dish_id)


@cooking_router.get("/dishes/by_type/{dish_type}")
async def get_dishes_by_type(dish_type: str):
    """
    Сложный эндпоинт: блюда по типу (суп, салат, основное блюдо, выпечка, напиток)
    """
    type_lower = dish_type.lower()
    result = {
        dish_id: dish for dish_id, dish in dishes.items() if dish["type"].lower() == type_lower
    }

    if not result:
        valid_types = set(d["type"] for d in dishes.values())
        raise HTTPException(
            status_code=404,
            detail=f"Блюда типа '{dish_type}' не найдены. Доступные типы: {', '.join(valid_types)}",
        )

    logger.info(f"Запрос блюд типа: {dish_type}")
    return result


@cooking_router.get("/dishes/by_country/{country}")
async def get_dishes_by_country(country: str):
    """
    Сложный эндпоинт: блюда указанной страны
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if country.lower() in dish["country"].lower()
    }

    if not result:
        raise HTTPException(status_code=404, detail=f"Блюда страны '{country}' не найдены")

    logger.info(f"Запрос блюд страны: {country}")
    return result


@cooking_router.get("/dishes/calories")
async def get_dishes_by_calories_range(min_calories: int = 0, max_calories: int = 1000):
    """
    Сложный эндпоинт: блюда в указанном диапазоне калорий
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if min_calories <= dish["calories"] <= max_calories
    }

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Блюда с калорийностью от {min_calories} до {max_calories} не найдены",
        )

    logger.info(f"Запрос блюд с калорийностью от {min_calories} до {max_calories}")
    return result


@cooking_router.get("/dishes/quick")
async def get_quick_dishes(max_minutes: int = 30):
    """
    Сложный эндпоинт: быстрые блюда (время приготовления не больше указанного)
    """
    result = {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if dish["cooking_time_minutes"] <= max_minutes
    }

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Блюда со временем приготовления до {max_minutes} минут не найдены",
        )

    logger.info(f"Запрос быстрых блюд (до {max_minutes} минут)")
    return result


@cooking_router.get("/food_info")
async def get_food_info():
    """
    Возвращает справочную информацию:
    - список всех стран, представленных в базе
    - список всех типов блюд
    - статистика по странам и типам
    """
    # Получаем уникальные страны
    countries = sorted(set(dish["country"] for dish in dishes.values()))

    # Получаем уникальные типы блюд
    dish_types = sorted(set(dish["type"] for dish in dishes.values()))

    # Считаем количество блюд по странам
    countries_count = {}
    for dish in dishes.values():
        country = dish["country"]
        countries_count[country] = countries_count.get(country, 0) + 1

    # Считаем количество блюд по типам
    types_count = {}
    for dish in dishes.values():
        dish_type = dish["type"]
        types_count[dish_type] = types_count.get(dish_type, 0) + 1

    return {
        "countries": countries,
        "dish_types": dish_types,
        "statistics": {
            "total_dishes": len(dishes),
            "by_country": countries_count,
            "by_type": types_count,
        },
    }
