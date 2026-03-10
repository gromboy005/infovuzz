import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
router = Router()

# ================= РАСШИРЕННАЯ БАЗА ДАННЫХ (V2) =================
DATA = {
    "it": {
        "name": "💻 IT и Программирование",
        "unis": {
            "mipt": {
                "name": "МФТИ", "url": "https://mipt.ru",
                "faculties": {
                    "fivt": {"name": "ФПМИ", "desc": "Прикладная математика и информатика", "exams": "Математика (П), Информатика, Русский", "budget": 290, "paid": 200},
                    "rt": {"name": "ФРТК", "desc": "Радиотехника и компьютерные технологии", "exams": "Математика (П), Физика, Русский", "budget": 285, "paid": 190},
                    "lfi": {"name": "ЛФИ", "desc": "Фундаментальная и прикладная физика", "exams": "Математика (П), Физика, Русский", "budget": 292, "paid": 210}
                }
            },
            "hse": {
                "name": "НИУ ВШЭ", "url": "https://hse.ru",
                "faculties": {
                    "fkn": {"name": "ФКН (ПМИ)", "desc": "Лучшие программисты по версии Яндекса.", "exams": "Математика (П), Информатика, Русский", "budget": 295, "paid": 210},
                    "se": {"name": "Программная инженерия", "desc": "Разработка сложных программных систем.", "exams": "Математика (П), Информатика, Русский", "budget": 294, "paid": 205},
                    "biz": {"name": "Бизнес-информатика", "desc": "Стык IT и менеджмента.", "exams": "Математика (П), Иностранный, Русский", "budget": 280, "paid": 190}
                }
            },
            "itmo": {
                "name": "Университет ИТМО", "url": "https://itmo.ru",
                "faculties": {
                    "ct": {"name": "Программная инженерия", "desc": "Разработка ПО и спортивное программирование.", "exams": "Математика (П), Информатика, Русский", "budget": 288, "paid": 195},
                    "fitip": {"name": "ФИТиП", "desc": "Информационные технологии и программирование.", "exams": "Математика (П), Информатика, Русский", "budget": 290, "paid": 200},
                    "ib": {"name": "Информационная безопасность", "desc": "Защита данных и криптография.", "exams": "Математика (П), Информатика, Русский", "budget": 282, "paid": 185}
                }
            },
            "msu": {
                "name": "МГУ (ВМК)", "url": "https://cs.msu.ru",
                "faculties": {
                    "pmi": {"name": "ПМИ", "desc": "Фундаментальная математика и код.", "exams": "Математика (П), Информатика, Русский + ДВИ", "budget": 350, "paid": 270},
                    "fiit": {"name": "ФИИТ", "desc": "Фундаментальная информатика.", "exams": "Математика (П), Информатика, Русский + ДВИ", "budget": 345, "paid": 260},
                    "mech": {"name": "Мехмат", "desc": "Классическая математика и механика.", "exams": "Математика (П), Физика, Русский + ДВИ", "budget": 335, "paid": 250}
                }
            },
            "bmstu": {
                "name": "МГТУ им. Баумана (ИУ)", "url": "https://bmstu.ru",
                "faculties": {
                    "iu7": {"name": "Программная инженерия (ИУ7)", "desc": "Элитная школа программистов Бауманки.", "exams": "Математика (П), Информатика, Русский", "budget": 285, "paid": 180},
                    "iu9": {"name": "Теоретическая информатика (ИУ9)", "desc": "Сложные вычисления и алгоритмы.", "exams": "Математика (П), Информатика, Русский", "budget": 282, "paid": 175},
                    "iu8": {"name": "Инф. безопасность (ИУ8)", "desc": "Защита автоматизированных систем.", "exams": "Математика (П), Информатика, Русский", "budget": 280, "paid": 170}
                }
            }
        }
    },
    "tech": {
        "name": "⚙️ Технологии и Инженерия",
        "unis": {
            "bmstu": {
                "name": "МГТУ им. Баумана", "url": "https://bmstu.ru",
                "faculties": {
                    "sm": {"name": "Специальное машиностроение", "desc": "Космос, ракеты и робототехника.", "exams": "Математика (П), Физика, Русский", "budget": 265, "paid": 170},
                    "rk": {"name": "Робототехника", "desc": "Автоматизация и мехатроника.", "exams": "Математика (П), Физика/Инфо, Русский", "budget": 275, "paid": 185},
                    "mt": {"name": "Машиностроительные технологии", "desc": "Инновационные материалы и оборудование.", "exams": "Математика (П), Физика, Русский", "budget": 240, "paid": 150}
                }
            },
            "spbpu": {
                "name": "СПбПУ (Политех)", "url": "https://spbstu.ru",
                "faculties": {
                    "immit": {"name": "ИММиТ", "desc": "Машиностроение и материалы.", "exams": "Математика (П), Физика, Русский", "budget": 245, "paid": 150},
                    "ice": {"name": "ИСИ", "desc": "Строительство и архитектура.", "exams": "Математика (П), Физика, Русский", "budget": 250, "paid": 160},
                    "energy": {"name": "Энергетика", "desc": "Электроэнергетика и электротехника.", "exams": "Математика (П), Физика, Русский", "budget": 248, "paid": 155}
                }
            },
            "mephi": {
                "name": "НИЯУ МИФИ", "url": "https://mephi.ru",
                "faculties": {
                    "phys": {"name": "Ядерные физика и технологии", "desc": "Атомная энергетика и исследования.", "exams": "Математика (П), Физика, Русский", "budget": 260, "paid": 175},
                    "laser": {"name": "Лазерные технологии", "desc": "Квантовая инженерия.", "exams": "Математика (П), Физика, Русский", "budget": 255, "paid": 160},
                    "icis": {"name": "Интеллектуальные киберсистемы", "desc": "ИИ и управление сложными системами.", "exams": "Математика (П), Информатика, Русский", "budget": 278, "paid": 190}
                }
            },
            "itmo_tech": {
                "name": "Университет ИТМО", "url": "https://itmo.ru",
                "faculties": {
                    "photon": {"name": "Фотоника", "desc": "Лазеры, оптика и сенсоры.", "exams": "Математика (П), Физика, Русский", "budget": 250, "paid": 155},
                    "robo": {"name": "Мехатроника и робототехника", "desc": "Умные системы управления.", "exams": "Математика (П), Информатика/Физика, Русский", "budget": 265, "paid": 170},
                    "biotech": {"name": "Биотехнологии", "desc": "Пищевая и биоинженерия.", "exams": "Химия/Биология, Математика (П), Русский", "budget": 235, "paid": 145}
                }
            },
            "tpu": {
                "name": "Томский Политех (ТПУ)", "url": "https://tpu.ru",
                "faculties": {
                    "oil": {"name": "Нефтегазовое дело", "desc": "Добыча и переработка ресурсов.", "exams": "Математика (П), Физика, Русский", "budget": 240, "paid": 140},
                    "power": {"name": "Электроэнергетика", "desc": "Современные энергосистемы.", "exams": "Математика (П), Физика, Русский", "budget": 235, "paid": 135}
                }
            }
        }
    },
    "science": {
        "name": "🔬 Естественные науки",
        "unis": {
            "msu": {
                "name": "МГУ им. Ломоносова", "url": "https://msu.ru",
                "faculties": {
                    "chem": {"name": "Химфак", "desc": "Классическое химическое образование.", "exams": "Химия, Математика (П), Русский + ДВИ", "budget": 350, "paid": 270},
                    "bio": {"name": "Биофак", "desc": "Фундаментальная биология.", "exams": "Биология, Математика (П), Русский + ДВИ", "budget": 340, "paid": 260},
                    "physics": {"name": "Физфак", "desc": "Все разделы современной физики.", "exams": "Физика, Математика (П), Русский + ДВИ", "budget": 345, "paid": 265},
                    "geo": {"name": "Геофак", "desc": "География и экология.", "exams": "География, Математика (П), Русский + ДВИ", "budget": 310, "paid": 230}
                }
            },
            "nsu": {
                "name": "НГУ", "url": "https://nsu.ru",
                "faculties": {
                    "phys": {"name": "Физфак", "desc": "Наука в Сибирском отделении РАН.", "exams": "Математика (П), Физика, Русский", "budget": 260, "paid": 160},
                    "fen": {"name": "ФЕН (Химия)", "desc": "Глубокое погружение в естественные науки.", "exams": "Химия, Математика (П), Русский", "budget": 255, "paid": 155},
                    "ggf": {"name": "ГГФ", "desc": "Геология и геофизика.", "exams": "Математика (П), Физика/География, Русский", "budget": 230, "paid": 140}
                }
            },
            "spbu": {
                "name": "СПбГУ", "url": "https://spbu.ru",
                "faculties": {
                    "geo": {"name": "Институт наук о Земле", "desc": "География, геология и картография.", "exams": "География, Математика (П), Русский", "budget": 245, "paid": 160},
                    "chem_spb": {"name": "Институт химии", "desc": "Современные материалы и синтез.", "exams": "Химия, Математика (П), Русский", "budget": 265, "paid": 170},
                    "bio_spb": {"name": "Биологический факультет", "desc": "Генетика и физиология.", "exams": "Биология, Химия, Русский", "budget": 260, "paid": 175}
                }
            }
        }
    },
    "med": {
        "name": "🩺 Медицина и Биоинженерия",
        "unis": {
            "sechenov": {
                "name": "Первый МГМУ (Сеченовский)", "url": "https://sechenov.ru",
                "faculties": {
                    "lech": {"name": "Лечебное дело", "desc": "Классическая медицина.", "exams": "Химия, Биология, Русский", "budget": 285, "paid": 185},
                    "stom": {"name": "Стоматология", "desc": "Самое популярное направление.", "exams": "Химия, Биология, Русский", "budget": 290, "paid": 210},
                    "pharm": {"name": "Фармация", "desc": "Разработка и производство лекарств.", "exams": "Химия, Биология, Русский", "budget": 260, "paid": 160},
                    "pediatr": {"name": "Педиатрия", "desc": "Врач-педиатр общего профиля.", "exams": "Химия, Биология, Русский", "budget": 270, "paid": 165}
                }
            },
            "pirogov": {
                "name": "РНИМУ им. Пирогова", "url": "https://rsmu.ru",
                "faculties": {
                    "ped": {"name": "Педиатрия", "desc": "Лечение детей и подростков.", "exams": "Химия, Биология, Русский", "budget": 270, "paid": 165},
                    "bio_med": {"name": "Медицинская кибернетика", "desc": "IT в медицине.", "exams": "Математика (П), Биология, Русский", "budget": 260, "paid": 150},
                    "dent": {"name": "Стоматология", "desc": "Современные методы протезирования.", "exams": "Химия, Биология, Русский", "budget": 288, "paid": 195}
                }
            }
        }
    }
}

# ================= CALLBACK DATA =================
class Nav(CallbackData, prefix="v3"):
    level: str
    prof: str = ""
    uni: str = ""
    fac: str = ""
    info: str = ""

# ================= КЛАВИАТУРЫ =================
def kb_profiles():
    builder = InlineKeyboardBuilder()
    for k, v in DATA.items():
        builder.button(text=v["name"], callback_data=Nav(level="unis", prof=k))
    builder.button(text="🛑 Выйти", callback_data="exit")
    builder.adjust(1)
    return builder.as_markup()

def kb_unis(prof_key):
    builder = InlineKeyboardBuilder()
    for k, v in DATA[prof_key]["unis"].items():
        builder.button(text=f"🏛 {v['name']}", callback_data=Nav(level="facs", prof=prof_key, uni=k))
    builder.button(text="⬅️ К направлениям", callback_data=Nav(level="start"))
    builder.adjust(1)
    return builder.as_markup()

def kb_facs(prof_key, uni_key):
    builder = InlineKeyboardBuilder()
    for k, v in DATA[prof_key]["unis"][uni_key]["faculties"].items():
        builder.button(text=f"🎓 {v['name']}", callback_data=Nav(level="menu", prof=prof_key, uni=uni_key, fac=k))
    builder.button(text="⬅️ К списку вузов", callback_data=Nav(level="unis", prof=prof_key))
    builder.adjust(1)
    return builder.as_markup()

def kb_fac_menu(prof, uni, fac):
    builder = InlineKeyboardBuilder()
    builder.button(text="📖 Экзамены", callback_data=Nav(level="info", prof=prof, uni=uni, fac=fac, info="exams"))
    builder.button(text="📊 Проходные баллы", callback_data=Nav(level="info", prof=prof, uni=uni, fac=fac, info="scores"))
    builder.button(text="🌐 Сайт вуза", url=DATA[prof]["unis"][uni]["url"])
    builder.button(text="⬅️ К факультетам", callback_data=Nav(level="facs", prof=prof, uni=uni))
    builder.adjust(2)
    return builder.as_markup()

def kb_back_to_fac(prof, uni, fac):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад к факультету", callback_data=Nav(level="menu", prof=prof, uni=uni, fac=fac))
    return builder.as_markup()

# ================= ОБРАБОТЧИКИ =================
@router.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "👋 <b>Добро пожаловать в навигатор абитуриента!</b>\n\n"
        "Я помогу тебе определиться с будущим вузом и факультетом. Выбери интересующее направление подготовки ниже 👇",
        reply_markup=kb_profiles()
    )

@router.callback_query(Nav.filter(F.level == "start"))
async def back_to_start(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Выбери интересующее направление:</b>", 
        reply_markup=kb_profiles()
    )

@router.callback_query(Nav.filter(F.level == "unis"))
async def show_unis(call: CallbackQuery, callback_data: Nav):
    p_name = DATA[callback_data.prof]["name"]
    await call.message.edit_text(
        f"📍 <b>Направление: {p_name}</b>\n\n"
        "Выбери университет для просмотра доступных факультетов:",
        reply_markup=kb_unis(callback_data.prof)
    )

@router.callback_query(Nav.filter(F.level == "facs"))
async def show_facs(call: CallbackQuery, callback_data: Nav):
    uni = DATA[callback_data.prof]["unis"][callback_data.uni]
    await call.message.edit_text(
        f"🏛 <b>{uni['name']}</b>\n\n"
        "Выбери интересующий факультет или образовательную программу:",
        reply_markup=kb_facs(callback_data.prof, callback_data.uni)
    )

@router.callback_query(Nav.filter(F.level == "menu"))
async def fac_menu(call: CallbackQuery, callback_data: Nav):
    uni = DATA[callback_data.prof]["unis"][callback_data.uni]
    fac = uni["faculties"][callback_data.fac]
    await call.message.edit_text(
        f"🎓 <b>Факультет: {fac['name']}</b> ({uni['name']})\n\n"
        f"<i>{fac['desc']}</i>\n\n"
        "Что именно ты хочешь узнать?",
        reply_markup=kb_fac_menu(callback_data.prof, callback_data.uni, callback_data.fac)
    )

@router.callback_query(Nav.filter(F.level == "info"))
async def show_info(call: CallbackQuery, callback_data: Nav):
    fac = DATA[callback_data.prof]["unis"][callback_data.uni]["faculties"][callback_data.fac]
    
    if callback_data.info == "exams":
        text = f"📖 <b>Экзамены для поступления на {fac['name']}:</b>\n\n{fac['exams']}"
    else:
        text = (f"📊 <b>Проходные баллы на {fac['name']}:</b>\n\n"
                f"✅ Бюджет: от <b>{fac['budget']}</b> баллов\n"
                f"💳 Контракт: от <b>{fac['paid']}</b> баллов\n\n"
                f"<i>Указаны средние значения за прошлый год.</i>")
    
    await call.message.edit_text(
        text, 
        reply_markup=kb_back_to_fac(callback_data.prof, callback_data.uni, callback_data.fac)
    )

@router.callback_query(F.data == "exit")
async def exit_bot(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("📴 Бот выключен. Удачи в подготовке к экзаменам! Чтобы вернуться, нажми /start")

async def main():
    # Используем DefaultBotProperties для автоматического применения HTML парсера
    bot = Bot(
        token="8616359892:AAEqyOUSlMqhLq9LVAIb-7FZG5Et-H7V_Ik", # Не забудь поменять токен!
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    
    # Удаляем старые вебхуки, чтобы бот не выдавал ошибку Conflict
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")